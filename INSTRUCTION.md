# 去ai生成水印工具 - 使用指南

这个工具可以帮助你在局域网内用手机访问电脑，轻松去掉AI生成的简单水印（如Logo、文字）。

## 快速使用步骤

### 1. 准备环境

确保你已经在Windows电脑上安装了 Python。
在当前目录下运行（如果你是第一次使用）：

```bash
pip install -r requirements.txt
```

### 2. 启动服务

在当前目录的文件夹地址栏输入 `cmd` 或 `powershell`，然后输入以下命令：

```bash
streamlit run app.py
```

如果运行正确，你会看到类似这样的输出：

```example
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.100:8501
```

### 3. 手机使用

- 确保你的手机和运行这个程序的电脑连接的是**同一个 WiFi**。
- 在手机浏览器（Chrome/Safari）地址栏输入你在上面看到的 `Network URL`（比如 `http://192.168.1.100:8501`）。
- 就可以直接上传手机里的图片去水印了。

### 4. 操作步骤

1. 上传图片。
2. 在图片上涂抹（用手指在手机屏幕上画）那个讨厌的水印。
3. 点击“一键去除”。
4. 满意后长按图片或点击下载保存。

### ⚠️ 关于水印去除能力

- 这个版本使用的是 Open Source Computer Vision Library (OpenCV) 的快速修复算法（Telea）。
- ✅ **它擅长处理**：小范围的水印、简单的Logo、日期的去除。
- ❌ **它不擅长**：全屏的透明大水印（那种会完全遮挡内容的）、极其复杂的背景纹理修复。如果需要那种“神级”修复（如 LaMa 模型），电脑显卡需要更强配置。
