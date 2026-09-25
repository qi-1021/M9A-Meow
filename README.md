<div align="center">
<img alt="M9A-Meow Logo" src="logo.png" width="160" height="160" />

# M9A-Meow

**这是对于 [M9A (重返未来：1999 小助手)](https://github.com/MAA1999/M9A) 手机端的一种原生实现**

> 注：作者开发完就发现，M9A的开发者们已经在开发手机端了而且和这个几乎一摸一样，重复造轮子了属于是。不过，无妨。移植的经验可以运用在更多的开发中，我要去开发终末地MAAend的手机端了。 --isqi
> 
> 对了，M9A手机版内测群：1080177843，他们的实现也会在不久后上线。

基于 MaaFramework 与 Android 虚拟显示技术，《重返未来：1999》全日常一键长草！

[![GitHub Release](https://img.shields.io/github/v/release/qi-1021/M9A-Meow?style=flat-square&label=Latest)](https://github.com/qi-1021/M9A-Meow/releases/latest)
[![Build M9A-Meow APK](https://github.com/qi-1021/M9A-Meow/actions/workflows/build-apk.yml/badge.svg)](https://github.com/qi-1021/M9A-Meow/actions/workflows/build-apk.yml)
[![Auto-Sync Upstream M9A](https://github.com/qi-1021/M9A-Meow/actions/workflows/sync-upstream.yml/badge.svg)](https://github.com/qi-1021/M9A-Meow/actions/workflows/sync-upstream.yml)
[![License](https://img.shields.io/badge/License-AGPL%20v3.0-blue.svg?style=flat-square)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Android%209%2B-3DDC84?style=flat-square&logo=android&logoColor=white)](https://github.com/qi-1021/M9A-Meow)
[![Architecture](https://img.shields.io/badge/Arch-arm64--v8a%20%7C%20x86__64-orange?style=flat-square)](https://github.com/qi-1021/M9A-Meow)

[下载最新发布版 (Releases)](https://github.com/qi-1021/M9A-Meow/releases/latest) · [问题反馈](https://github.com/qi-1021/M9A-Meow/issues) · 联系邮箱: [qiisme1021@icloud.com](mailto:qiisme1021@icloud.com)

</div>

---

> 🐱 **这是对于 M9A 手机端的一种实现**：复用 [MAA-Meow](https://github.com/Aliothmoon/MAA-Meow) 核心开发者维护的 [MaaFwApp](https://github.com/Aliothmoon/MaaFwApp) 架构，无需 Root 权限（推荐通过 Shizuku 授权），游戏可在独立后台虚拟屏中静默运行，前台正常聊天、看视频，互不干扰！

---

## 🌟 特性一览

| 图标  | 特性                    | 详细说明                                                                                          |
|:---:|:--------------------- |:--------------------------------------------------------------------------------------------- |
| 🧠  | **原生运行 Python Agent** | 搭载专为 Android Bionic 编译的 **CPython 3.13 + MaaFramework** 运行时，完整执行 M9A 自定义识别器与动作，无需 PC 或第三方容器环境 |
| 🪟  | **双运行模式**             | **前台悬浮窗**：实时控制面板，轻量透明悬浮球<br>**后台虚拟屏**：在独立虚拟显示空间中静默挂机，支持实时小窗预览与全屏手操接管                          |
| 📦  | **完整 M9A 业务支持**       | 完整覆盖日常作战刷体力、荒原产出与角色好感度收获、签到领奖、心相整理、活动代币刷取、局外演绎、兑换码兑换等                                         |
| 🎮  | **全渠道服适配**            | 适配官服、Bilibili 服、OPPO 服、华为服、小米服、港澳台服、国际服（EN / JP / KR）等全部游戏客户端                                 |
| ⏱️  | **定时与熄屏自动化**          | 支持周日程定时触发，后台挂机可自动锁屏防误触；支持定时自动亮屏并输入锁屏数字 PIN 码唤醒                                                |
| 🔔  | **全渠道通知推送**           | 任务完成或异常时，可实时推送至 Server酱、Telegram、Discord、钉钉、Bark、Gotify、SMTP 邮件等                              |
| ☁️  | **纯云端 CI 编译**         | 配套完备的 GitHub Actions 流水线，出包全在云端完成，**无需在本地配置数 GB 的 Android SDK / NDK 编译工具**                    |

---

## 📱 运行要求

| 项目       | 要求                                              | 说明                                        |
|:-------- |:----------------------------------------------- |:----------------------------------------- |
| **操作系统** | Android 9.0（API 28）及以上                          | 推荐 Android 11+，后台虚拟空间兼容性更佳                |
| **提权方案** | [Shizuku](https://shizuku.rikka.app/) 或 Root 权限 | 推荐使用 Shizuku，免 Root 即可直接调用系统底层 Native 控制器 |
| **设备架构** | `arm64-v8a`（主流真机） / `x86_64`（PC 模拟器）            | 默认提供单架构轻量化包，安装包由 260MB+ 缩减至约 120MB        |
| **目标游戏** | 《重返未来：1999》客户端                                  | 手机需安装与所选配置对应的游戏渠道服客户端                     |

---

## 📌 版本锚定与依赖清单

为了保证后续维护时能够清晰对齐上游更新，下表详细记录了本项目当前固定的所有核心组件版本与 Commit。该清单同步记录在项目根目录的 [`UPSTREAM_VERSIONS.json`](UPSTREAM_VERSIONS.json) 中：

| 组件名称                      | 来源仓库                                                                                | 当前锚定版本 / Commit                                                                                                                    | 作用说明                                                                                  |
|:------------------------- |:----------------------------------------------------------------------------------- |:---------------------------------------------------------------------------------------------------------------------------------- |:------------------------------------------------------------------------------------- |
| **M9A**                   | [MAA1999/M9A](https://github.com/MAA1999/M9A)                                       | Commit [`acce2d4`](https://github.com/MAA1999/M9A/commit/acce2d434bfbd72c1af42af2908baf33665c8a04)<br>(Tag: `v4.9.0-28-gacce2d43`) | 业务资源仓库，提供 `interface.json`、Pipeline 流水线、图片模板、各渠道服资源及 Python Agent 业务逻辑                |
| **MaaFramework**          | [MaaXYZ/MaaFramework](https://github.com/MaaXYZ/MaaFramework)                       | Tag `v5.14.0`<br>(向前兼容 `v5.13.1`+)                                                                                                 | 核心自动化框架动态库（`libMaaFramework.so`、`libMaaUtils.so`、`libMaaAndroidNativeControlUnit.so`） |
| **MaaAgentCoreAndroid**   | [Aliothmoon/MaaAgentCoreAndroid](https://github.com/Aliothmoon/MaaAgentCoreAndroid) | Tag `3.13.15-maafw5.12.3`                                                                                                          | 专为 Android 交叉编译的 CPython 3.13.15 运行时核心库、标准库及 MaaFramework Python 基础绑定                 |
| **MaaCommonAssets (OCR)** | [MaaXYZ/MaaCommonAssets](https://github.com/MaaXYZ/MaaCommonAssets)                 | `OCR/ppocr_v6/small`<br>(ONNX 格式)                                                                                                  | 轻量级 PP-OCR v6 模型文件（`det.onnx`, `rec.onnx`, `keys.txt`）                                |
| **Android 宿主工程**          | [Aliothmoon/MaaFwApp](https://github.com/Aliothmoon/MaaFwApp)                       | 与 [MAA-Meow](https://github.com/Aliothmoon/MAA-Meow) 核心同源                                                                          | 提供 Jetpack Compose 界面、Shizuku 进程代理、虚拟显示屏与多点触控控制器                                      |

### 构建工具链基线

```properties
JDK: OpenJDK 17 (Temurin)
Android SDK: compileSdk 37, targetSdk 36, minSdk 28
Android NDK: 27.2.12479018 (r27c)
CMake: 3.22.1
Android Gradle Plugin (AGP): 9.2.1
Kotlin: 2.3.21 / KSP: 2.3.9
Python (构建侧): 3.12+ (本地与 CI) / 3.13 (手机运行侧)
```

---

## 🔄 上游版本升级指南

当未来 M9A 官方发布了新功能、新活动，或者底层 MaaFramework 升级时，请按照以下步骤更新：

### 场景 1：自动巡检更新（推荐，全自动无需操作）

仓库内置了 [`.github/workflows/sync-upstream.yml`](.github/workflows/sync-upstream.yml) 巡检流水线，每天北京时间 **10:00** 与 **22:00** 自动检查上游是否有新提交。若检测到更新，会自动拉取最新资源并重新编译打包 APK。

你也可以在 GitHub Actions 页面随时手动触发该流程：

- 进入 Actions -> **Auto-Sync Upstream M9A** -> **Run workflow**。

---

### 场景 2：手动更新 M9A 上游业务资源

当希望立即在本地跟进 M9A 官方的日常或活动变动时：

```bash
# 1. 自动同步脚本（自动拉取 M9A 最新提交并刷新 OCR 与版本配置）
python scripts/sync_upstream.py

# 2. 提交更新并推送到 GitHub
git add upstream/m9a UPSTREAM_VERSIONS.json README.md
git commit -m "chore(upstream): bump m9a to $(git -C upstream/m9a rev-parse --short HEAD)"
git push origin main
```

> 推送至 GitHub 后，GitHub Actions 会**自动触发云端编译**，数分钟后即可在 Actions 页面下载新版 APK！

---

### 场景 3：更新 MaaFramework 核心动态库

当 MaaFramework 发布了新版本（例如 `v5.15.0`）：

1. **方式 A：通过 GitHub Actions 界面手动指定**
   - 进入 GitHub 仓库页面，点击 **Actions** -> **Build M9A-Meow APK** -> **Run workflow**；
   - 在 `MaaFramework Tag` 输入框中填入目标版本（例如 `v5.15.0`），点击开始构建即可。
2. **方式 B：更新本地配置**
   - 修改 [`.github/workflows/build-apk.yml`](.github/workflows/build-apk.yml) 或在本地执行：
     
     ```bash
     python scripts/setup_maa_framework.py --tag v5.15.0 --abi arm64-v8a
     ```
   - 同步更新 [`UPSTREAM_VERSIONS.json`](UPSTREAM_VERSIONS.json) 中的记录。

---

### 场景 4：更新 Python Agent 运行时依赖

如果 M9A 在其 `requirements.txt` 中添加或变更了 Python 第三方依赖：

1. 检查 `upstream/m9a/requirements.txt`；
2. 如果新增了包含 C 扩展的原生轮子（如 Pillow 等），确认 [Chaquopy Android PyPI 镜像源](https://chaquo.com/pypi-13.1/) 是否提供对应 Android 轮子并在 [`scripts/build_agent_bundle.py`](scripts/build_agent_bundle.py) 中追加；
3. 如果是纯 Python 包（Pure Python），无需任何特殊配置，CI 组装脚本会自动将其打包进 `pure.zip`。

---

## 🚀 获取与构建方式

### 方式 A：云端自动构建（强烈推荐）

无需在本地电脑配置任何编译器或交叉环境，全程由 GitHub Actions 云端完成：

1. **触发构建**：
   - 每次向 `main` 分支执行 `git push` 会自动触发编译；
   - 也可在 GitHub 网页端点击 **Actions** -> **Build M9A-Meow APK** -> **Run workflow** 手动选择架构（`arm64-v8a` 或 `universal`）触发构建。
2. **下载安装包**：
   - 构建完成（约 3~5 分钟）后，在构建详情页最下方的 **Artifacts** 区域直接下载 `M9A-Meow-APKs`。

---

### 方式 B：本地开发构建（可选）

如需在本地调试 Android 源码，请先安装配置好 JDK 17、Android SDK Platform 37、NDK r27c 和 Python 3.12+。

> 严格隔离规范：所有中间产物与临时文件均保存在项目内目录（`.tmp/`、`.maa-cache/`、`.maafw/`、`agent-dist/`），**绝对不会污染操作系统的 `/tmp` 目录**。

```bash
# 1. 初始化 M9A 资源与 OCR 模型
python scripts/prepare_m9a.py

# 2. 拉取 MaaFramework Android 原生库
python scripts/setup_maa_framework.py --abi arm64-v8a

# 3. 组装 Android Python Agent 运行时
python scripts/build_agent_bundle.py \
  --out agent-dist \
  --requirements upstream/m9a/requirements.txt \
  --no-deps \
  --exclude pillow --require pillow==11.0.0 \
  --extra-index-url https://chaquo.com/pypi-13.1/ \
  --abi arm64-v8a

# 4. 编译 Debug APK
./gradlew assembleDebug
```

产物位置：`app/build/outputs/apk/debug/`

---

## 📂 项目工程结构

```text
Projects/M9A-Meow/
├── upstream/m9a/             # [子模块] M9A 官方资源库 (interface.json, tasks, resource, agent)
├── app/                      # Android 核心应用模块 (Compose 界面, 虚拟屏幕, Shizuku 桥)
├── build-logic/              # Gradle 插件集合 (配方解析, 资产注入, Agent 打包)
├── scripts/
│   ├── prepare_m9a.py        # M9A 资源、OCR 识别模型与图标提取脚本
│   ├── build_agent_bundle.py # Android Python 3.13 解释器与依赖组装工具
│   ├── setup_maa_framework.py# MaaFramework Android 原生动态库拉取脚本
│   └── sync_upstream.py      # 上游自动比对、同步与记录刷新引擎
├── .github/workflows/
│   ├── build-apk.yml         # GitHub Actions 云端打包工作流
│   └── sync-upstream.yml     # 上游自动巡检与级联构建流水线
├── UPSTREAM_VERSIONS.json    # 上游依赖与版本锚定元数据（机读与人读统一标准）
├── pi-profile.yaml           # M9A-Meow Android 打包配方配置
├── logo.png                  # 应用 256x256 高清启动图标
├── ENVIRONMENT.md            # 项目环境与隔离规范说明文档
└── README.md                 # 项目详细说明文档
```

---

## 📜 致谢与开源许可

- 本项目采用 **[AGPL-3.0](LICENSE)** 许可证开源。
- 业务自动化逻辑源自 **[MAA1999/M9A](https://github.com/MAA1999/M9A)**（遵循 AGPL-3.0）。
- Android 宿主架构与虚拟屏核心源自 **[Aliothmoon/MaaFwApp](https://github.com/Aliothmoon/MaaFwApp)** 与 **[Aliothmoon/MAA-Meow](https://github.com/Aliothmoon/MAA-Meow)**（遵循 AGPL-3.0）。
- 底层识别框架由 **[MaaXYZ/MaaFramework](https://github.com/MaaXYZ/MaaFramework)**（遵循 LGPL-3.0）提供。
- 特权服务调用由 **[RikkaApps/Shizuku](https://github.com/RikkaApps/Shizuku)** 提供支持。
