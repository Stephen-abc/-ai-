import streamlit as st
from streamlit_drawable_canvas import st_canvas
import cv2
import numpy as np
from PIL import Image
import io
import socket

# 设置页面配置
st.set_page_config(
    page_title="AI去除水印工具",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

def get_local_ip():
    """获取本机局域网IP"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 不需要这真连接，只是为了获取IP
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

# 获取本机IP用于提示用户
local_ip = get_local_ip()

# 侧边栏配置
with st.sidebar:
    st.header("⚙️ 设置")
    stroke_width = st.slider("笔刷大小", 1, 50, 20)
    st.markdown("---")
    st.markdown(f"### 📱 手机访问指南")
    st.markdown("确保手机和电脑在**同一WiFi**下。")
    st.markdown(f"在手机浏览器输入：\n**http://{local_ip}:8501**")
    st.markdown("---")
    st.markdown("### 💡 使用说明")
    st.markdown("1. 上传带有水印的图片")
    st.markdown("2. 在图片上**涂抹**需要去除的水印区域")
    st.markdown("3. 点击“一键去水印”")

st.title("🎨 AI 去除水印工具 (简单版)")
st.markdown("适用于去除 Logo、日期、文字等简单水印。")

# 步骤1：上传图片
uploaded_file = st.file_uploader("选择一张图片:", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # 读取图片
    image_bytes = uploaded_file.read()
    image = Image.open(io.BytesIO(image_bytes))
    
    # 转换为numpy数组用于opencv处理
    # 注意：PIL是RGB，OpenCV是BGR，Canvas返回是RGBA
    img_array = np.array(image)
    
    # 获取图片尺寸，调整canvas大小
    # 为了防止图片过大撑爆屏幕，可以限制显示宽度，但处理用原图
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("第一步：涂抹水印")
        
        # 创建绘图板
        canvas_result = st_canvas(
            fill_color="rgba(255, 165, 0, 0.3)",  # 填充颜色（这里没用到，因为是freedraw）
            stroke_width=stroke_width,
            stroke_color="#FFFFFF",
            background_image=image,
            update_streamlit=True,
            height=image.height if image.height < 800 else 800, # 限制最大高度
            width=image.width if image.width < 800 else 800,   # 简单处理，实际应该按比例
            drawing_mode="freedraw",
            key="canvas",
        )

    # 步骤2：处理
    if canvas_result.image_data is not None:
        # 获取掩膜（用户画的白色笔迹）
        mask_data = canvas_result.image_data
        
        # 提取Alpha通道作为掩膜，或者直接看颜色
        # canvas_result.image_data 是 RGBA，笔刷是白色 #FFFFFF
        # 我们只需要提取画了东西的地方。
        
        # 转换为灰度图
        mask = mask_data[:, :, 3] #取Alpha通道
        
        # 二值化，确保掩膜清晰
        _, mask = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY)
        
        # 确保尺寸一致（防止Resize导致的问题，虽然background_image保证了比例，但以防万一）
        if mask.shape[:2] != img_array.shape[:2]:
            mask = cv2.resize(mask, (img_array.shape[1], img_array.shape[0]))
        
        with col2:
            st.subheader("第二步：效果预览")
            process_btn = st.button("✨ 一键去水印", type="primary")
            
            if process_btn:
                with st.spinner("正在处理中..."):
                    # 转换图像格式 RGB -> BGR (OpenCV使用)
                    img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
                    
                    # 图像修复算法
                    # INPAINT_TELEA: 基于快速行进算法（通常效果较好）
                    # INPAINT_NS: 基于Navier-Stokes方程
                    inpainted_img = cv2.inpaint(img_bgr, mask, 3, cv2.INPAINT_TELEA)
                    
                    # 转换回 RGB
                    result_rgb = cv2.cvtColor(inpainted_img, cv2.COLOR_BGR2RGB)
                    
                    # 显示结果
                    st.image(result_rgb, caption="去水印结果")
                    
                    # 转换用于下载
                    result_pil = Image.fromarray(result_rgb)
                    buf = io.BytesIO()
                    result_pil.save(buf, format="PNG")
                    byte_im = buf.getvalue()
                    
                    st.download_button(
                        label="⬇️ 下载处理后的图片",
                        data=byte_im,
                        file_name="watermark_removed.png",
                        mime="image/png"
                    )
            else:
                st.info("请在左侧图片上涂抹水印区域，然后点击上方按钮。")

else:
    st.info("👋 请先上传一张图片开始。手机用户可以点击左上角箭头展开菜单查看连接方式。")
