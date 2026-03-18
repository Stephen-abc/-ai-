# AI 去水印移动应用 (构建指南)

您现在拥有了开发一款真正的手机 App（支持 Android 和 iOS）所需的全部**源代码**。

## 📱 核心功能

新版代码已经支持：

1. **自动检测最新图片提示**：App 启动时会弹窗询问是否处理最新图片。
2. **双模式选择**：支持“确认处理”（单张）或“选多张”（进入相册）。
3. **完全本地运行**：通过 OpenCV.js 实现本地处理，不需要电脑参与，不上传服务器。

## ⚠️ 关于 "安装包" 的重要说明

作为 AI，我无法直接生成二进制文件（即 `.apk` 或 `.ipa` 文件），因为这些文件需要通过复杂的**编译环境**（如 Android Studio 或 Xcode）生成。

但是，我已经为您准备好了**所有的源代码**和**配置文件** (`package.json`, `capacitor.config.json`)。

如果您希望得到可以直接安装的包，您有以下两种选择：

### 方案 A：找人或使用云端打包 (推荐，无需配置环境)

您可以将 `mobile-webapp` 文件夹打包发送给会开发的朋友，或者使用在线服务（如 PhoneGap Build 或 Ionic Appflow，但这通常需要账号）。

### 方案 B：自己动手编译 (如果您愿意尝试)

如果您想自己生成 `app-release.apk`，请按以下步骤操作（以 Android 为例）：

1. **安装 Node.js**: [https://nodejs.org](https://nodejs.org)
2. **安装 Android Studio**: [https://developer.android.com/studio](https://developer.android.com/studio)
3. **在 `mobile-webapp` 文件夹下打开终端**，运行：

```bash
# 1. 安装依赖
npm install

# 2. 初始化 Android 平台
npx cap add android

# 3. 将网页代码同步到原生项目
npx cap sync

# 4. 打开 Android Studio 进行构建
npx cap open android
```

1. 在 Android Studio 中，点击菜单栏的 `Build` -> `Build Bundle(s) / APK(s)` -> `Build APK(s)`。
2. 完成后，您就可以在输出目录找到 `app-debug.apk`，发送到手机即可安装！

## 📄 目录结构

- `index.html`: 主程序界面
- `script.js`: 核心逻辑 (已包含最新图片弹窗逻辑)
- `package.json`: 项目依赖配置
- `capacitor.config.json`: Capacitor 配置文件
