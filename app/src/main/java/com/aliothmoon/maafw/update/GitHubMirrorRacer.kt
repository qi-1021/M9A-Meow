package com.aliothmoon.maafw.update

import com.aliothmoon.maafw.constant.MiscConstants
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.async
import kotlinx.coroutines.coroutineScope
import kotlinx.coroutines.withContext
import kotlinx.coroutines.withTimeoutOrNull
import okhttp3.OkHttpClient
import okhttp3.Request
import timber.log.Timber
import java.util.concurrent.TimeUnit

/**
 * GitHub 下载镜像站竞速选择器
 *
 * 对给定的 GitHub release 下载 URL，并发 HEAD 探测各镜像站的替换 URL，
 * 选出响应最快（首个返回 2xx/3xx）的镜像站，返回替换后的下载地址。
 * 若全部失败或超时，则回退原始 URL。
 *
 * 镜像站工作原理：大多数站点接受 `https://<mirror>/<原始GitHub URL>` 这种前缀拼接的格式。
 */
internal object GitHubMirrorRacer {

    /**
     * 已知公开 GitHub 镜像站前缀，按推荐顺序排列
     * 每个前缀拼上原始 URL 即是镜像 URL，例如：
     *   https://ghproxy.com/https://github.com/owner/repo/releases/download/...
     */
    val DEFAULT_MIRRORS: List<String> = listOf(
        "https://ghproxy.com/",
        "https://mirror.ghproxy.com/",
        "https://ghfast.top/",
        "https://github.moeyy.xyz/",
        "https://gh.api.99988866.xyz/",
        "https://hub.whtrys.space/",
        "https://download.fastgit.org/",
        "https://gh-proxy.com/",
    )

    /** 单个镜像站 HEAD 探测超时 */
    private const val PROBE_TIMEOUT_MS = 4_000L

    /** 全部镜像竞速的总超时（若超时则用原始 URL） */
    private const val RACE_TIMEOUT_MS = 6_000L

    private val probeClient: OkHttpClient by lazy {
        OkHttpClient.Builder()
            .connectTimeout(PROBE_TIMEOUT_MS, TimeUnit.MILLISECONDS)
            .readTimeout(PROBE_TIMEOUT_MS, TimeUnit.MILLISECONDS)
            .writeTimeout(PROBE_TIMEOUT_MS, TimeUnit.MILLISECONDS)
            .followRedirects(true)
            .addInterceptor { chain ->
                val req = chain.request().newBuilder()
                    .header("User-Agent", MiscConstants.BROWSER_UA)
                    .build()
                chain.proceed(req)
            }
            .build()
    }

    /**
     * 对 [originalUrl]（形如 `https://github.com/...`）并发探测各镜像站，
     * 返回响应最快的镜像替换 URL，若全部失败则返回 [originalUrl] 本身。
     *
     * @param mirrors 要探测的镜像前缀列表，默认 [DEFAULT_MIRRORS]
     */
    suspend fun race(
        originalUrl: String,
        mirrors: List<String> = DEFAULT_MIRRORS,
    ): String {
        // 若非 GitHub URL，直接返回原始
        if (!originalUrl.contains("github.com", ignoreCase = true)) {
            return originalUrl
        }
        if (mirrors.isEmpty()) return originalUrl

        Timber.tag("MirrorRacer").d("Racing %d mirrors for: %s", mirrors.size, originalUrl)

        val winner = withTimeoutOrNull(RACE_TIMEOUT_MS) {
            raceInternal(originalUrl, mirrors)
        }

        return if (winner != null) {
            Timber.tag("MirrorRacer").i("Selected mirror: %s", winner)
            winner
        } else {
            Timber.tag("MirrorRacer").w("All mirrors timed out, falling back to original")
            originalUrl
        }
    }

    /**
     * 并发探测所有镜像，返回首个成功者的 URL（镜像 URL）；全部失败返回 null
     */
    private suspend fun raceInternal(originalUrl: String, mirrors: List<String>): String? =
        coroutineScope {
            // 为每个镜像站建一个 async job
            val probes = mirrors.map { prefix ->
                val mirrorUrl = prefix + originalUrl
                async(Dispatchers.IO) {
                    probe(mirrorUrl)?.let { mirrorUrl }
                }
            }

            // 逐个等待，首个非 null 即获胜
            var winner: String? = null
            for (probe in probes) {
                val result = probe.await()
                if (result != null && winner == null) {
                    winner = result
                    // 取消剩余任务
                    probes.forEach { it.cancel() }
                    break
                }
            }
            winner
        }

    /**
     * HEAD 探测 [url]，返回 2xx/3xx 时的最终落点（follow redirect 后的 URL），失败返回 null
     */
    private fun probe(url: String): String? = try {
        val request = Request.Builder()
            .url(url)
            .head()
            .header("User-Agent", MiscConstants.BROWSER_UA)
            .build()
        probeClient.newCall(request).execute().use { response ->
            val code = response.code
            Timber.tag("MirrorRacer").d("  %s -> %d", url, code)
            if (code in 200..399) url else null
        }
    } catch (e: Exception) {
        Timber.tag("MirrorRacer").v("  probe failed %s: %s", url, e.message)
        null
    }

    /**
     * 快速探测多个镜像并报告每个延迟（毫秒），供调试用
     * key = 镜像前缀，value = 延迟 ms（null 表示失败）
     */
    suspend fun benchmark(
        originalUrl: String,
        mirrors: List<String> = DEFAULT_MIRRORS,
    ): Map<String, Long?> {
        if (!originalUrl.contains("github.com", ignoreCase = true)) return emptyMap()

        return withContext(Dispatchers.IO) {
            mirrors.associateWith { prefix ->
                val mirrorUrl = prefix + originalUrl
                val start = System.currentTimeMillis()
                val ok = probe(mirrorUrl) != null
                if (ok) System.currentTimeMillis() - start else null
            }
        }
    }
}
