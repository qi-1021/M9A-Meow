# M9A-Android

《重返未来：1999》小助手 Android 版，支持全日常自动化、后台虚拟空间挂机与定时执行！

本项目将 [M9A (Assistant For Reverse: 1999)](https://github.com/MAA1999/M9A) 移植并打包为 Android 独立应用。底层复用与 [MAA-Meow](https://github.com/Aliothmoon/MAA-Meow) 相同的 Android 宿主架构与 [MaaFwApp](https://github.com/Aliothmoon/MaaFwApp) 特权运行体系。

## ✨ 特性

- **M9A 完整能力**：
  - 继承 M9A 官方 Project Interface V2 的全部日常任务、作战、荒原、签到、领奖、活动刷取等；
  - 搭载专为 Android 适配的 CPython 3.13 + MaaFramework Python Agent 运行时（支持自定义识别与动作）。
- **MAA-Meow 同款体验**：
  - **特权提权**：支持 [Shizuku](https://shizuku.rikka.app/) 或 Root 双模式，Native 控制器直连，完全无需 ADB 调试端口；
  - **后台虚拟屏**：在独立虚拟显示屏中无感运行游戏，前台手机可正常聊天、看视频，支持实时小窗预览与全屏接管；
  - **自动锁屏与息屏挂机**：任务完成后自动清理，支持定时唤醒、PIN 码自动解锁；
  - **定时执行与多通道推送**：支持周日程定时，完成后可推送至 Server酱、Telegram、Discord、钉钉、Bark、SMTP 邮件等。

## 📱 运行要求

| 项目 | 要求 |
|:---|:---|
| 系统 | Android 9（API 28）及以上 |
| 提权方式 | [Shizuku](https://shizuku.rikka.app/) 或 Root 权限（推荐 Shizuku，免 Root 亦可使用） |
| 架构支持 | `arm64-v8a`（主流手机） / `x86_64`（PC 安卓模拟器） |
| 游戏客户端 | 手机需安装《重返未来：1999》（官服 / B 服 / OPPO 服等） |

## 🚀 云端编译出包（推荐）

为了避免本地下载数 GB 的 Android SDK、NDK、CMake 和 Python 交叉编译工具链，本项目已配置好完整的 **GitHub Actions CI/CD 流水线**，全流程在云端完成编译：

1. **推送至 GitHub**：
   在 GitHub 上创建个人仓库（例如 `qi-1021/M9A-Android`），将本项目推送到仓库：
   ```bash
   git remote set-url origin https://github.com/<你的用户名>/M9A-Android.git
   git push -u origin main
   ```
2. **触发云端构建**：
   - 方式 A：进入 GitHub 仓库页面，点击 **Actions** -> **Build M9A Android APK** -> **Run workflow** 手动触发构建；
   - 方式 B：打 Tag 推送（例如 `git tag v1.0.0 && git push origin v1.0.0`），云端自动编译并生成 GitHub Release 发布包。
3. **下载 APK**：
   编译完成后（约 3-5 分钟），在 Actions 构建详情的 **Artifacts** 区域或 **Releases** 页面即可直接下载打包好的 `.apk` 安装包。

## 🛠️ 本地开发与构建（可选）

如需在本地构建，请确保已安装 JDK 17、Android SDK & NDK r27c、Python 3.12+：

```bash
# 1. 准备 M9A 资源、OCR 识别模型与图标
python scripts/prepare_m9a.py

# 2. 下载 MaaFramework 核心原生库 (以 arm64 为例)
python scripts/setup_maa_framework.py --abi arm64-v8a

# 3. 构建 Android Python Agent 运行时 Bundle
python scripts/build_agent_bundle.py \
  --out agent-dist \
  --requirements upstream/m9a/requirements.txt \
  --no-deps \
  --exclude pillow --require pillow==11.0.0 \
  --extra-index-url https://chaquo.com/pypi-13.1/ \
  --abi arm64-v8a

# 4. 构建 APK
./gradlew assembleDebug
```
产物位置：`app/build/outputs/apk/debug/`

> **注意**：本地脚本严格遵守项目隔离规范，所有临时文件与构建缓存均放在项目目录内（`.tmp/`、`.maa-cache/`、`.maafw/`），不会向系统 `/tmp` 产生残留。

## 📂 项目结构

```text
Projects/M9A-Android/
├── upstream/m9a/             # M9A 上游资源子模块 (tasks, resource, agent, interface.json)
├── app/                      # Android 主模块 (Compose UI, 虚拟显示器, Shizuku/Root 服务)
├── build-logic/              # Gradle 插件 (PI 资源自动打进 APK, Agent Bundle 组装)
├── scripts/
│   ├── prepare_m9a.py        # M9A 资源、OCR 模型与配置准备
│   ├── build_agent_bundle.py # Android Python 3.13 运行时构建工具
│   └── setup_maa_framework.py# MaaFramework Android 原生库下载工具
├── .github/workflows/
│   └── build-apk.yml         # GitHub Actions 云端构建流水线
├── pi-profile.yaml           # M9A Android 打包配方
└── logo.png                  # 应用图标
```

## 📜 许可证与致谢

- 本项目遵循 **AGPL-3.0** 开源许可证。
- 自动化内核与 Android 宿主架构源自 [MaaFramework](https://github.com/MaaXYZ/MaaFramework)、[MAA-Meow](https://github.com/Aliothmoon/MAA-Meow) 与 [MaaFwApp](https://github.com/Aliothmoon/MaaFwApp)。
- 游戏识别资产与 Agent 逻辑来自 [M9A](https://github.com/MAA1999/M9A)。
