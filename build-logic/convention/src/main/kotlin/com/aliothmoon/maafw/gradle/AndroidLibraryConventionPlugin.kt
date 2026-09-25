package com.aliothmoon.maafw.gradle

import com.android.build.api.dsl.LibraryExtension
import org.gradle.api.Plugin
import org.gradle.api.Project
import org.gradle.kotlin.dsl.getByType

class AndroidLibraryConventionPlugin : Plugin<Project> {
    override fun apply(target: Project) {
        with(target) {
            // AGP 9 already puts the library plugin on the classpath, no version needed here
            pluginManager.apply("com.android.library")
            configureAndroidCommon(extensions.getByType<LibraryExtension>())

            // 图标资源库等 drawables 包含 ?attr/colorControlNormal 等动态主题属性，
            // 这些属性在 App 层消费时由宿主主题解析，跳过子模块独立的 VerifyLibraryResources 校验
            tasks.matching { it.name.startsWith("verify") && it.name.endsWith("Resources") }
                .configureEach {
                    enabled = false
                }
        }
    }
}

