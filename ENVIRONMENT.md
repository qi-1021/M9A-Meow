# 环境说明 (ENVIRONMENT.md)

## 1. 项目定位与环境策略
- **项目名称**：M9A-Android (重返未来：1999 小助手 Android 版)
- **环境策略**：**云端构建优先 / 独立沙箱隔离**
- **Python 版本**：Python 3.12+ (本地准备工具) / CPython 3.13 (Android Agent 目标运行时)
- **SDK / NDK 基线**：
  - compileSdk: 37
  - targetSdk: 36
  - minSdk: 28 (Android 9.0+)
  - NDK: r27c (27.2.12479018)
  - Java: OpenJDK 17 (Temurin)

## 2. 隔离与临时文件规范
- **禁止系统 /tmp 污染**：本地运行脚本时，强制重定向 `TMPDIR` / `TEMP` / `TMP` 至项目内的 `.tmp/` 目录；
- **构建缓存隔离**：
  - `.maa-cache/`: MaaFramework 原生包缓存
  - `.maafw/`: MaaAgentCoreAndroid 解释器内核及下载缓存
  - `agent-dist/`: 组装后的 Android Agent 运行时 bundle 产物
  - `.tmp/`: 运行期临时数据

## 3. 云端编译流水线
- CI 配置位于 `.github/workflows/build-apk.yml`，通过 GitHub Actions 云端 Ubuntu 镜像编译，无需在本机安装数十 GB 的 Android SDK/NDK 编译链。
