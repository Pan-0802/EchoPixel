import gradio as gr
import requests
import base64
import io
import json
from PIL import Image
# 假设你已经按照之前的建议在 engine 目录下创建了感知模块
# from engine.perception import get_image_perception 

# --- 工具函数：Base64 转换 ---
def pil_to_base64(img):
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

# --- 核心业务逻辑：EchoPixel Agent 流转 ---
def echo_pixel_pipeline(input_img):
    if input_img is None:
        return "请先上传一张照片...", None

    # 1. 模拟感知与剧情
    thought_chain = "【感知引擎】识别到：西南大学图书馆背景...\n"
    thought_chain += "【决策引擎】构思：一个小机器人在书架前寻找代码秘籍...\n"
    
    # 2. 调用你之前验证成功的 API 逻辑
    url = "http://127.0.0.1:7860/sdapi/v1/txt2img"
    payload = {
        # 加上你之前下载的 LoRA 文件名
        "prompt": "pixel art, a small robot in a library, <lora:Pony6.sakuemonq.10:1>",
        "negative_prompt": "blur, lowres, realistic",
        "steps": 20,
        "width": 512,
        "height": 512
    }
    
    try:
        response = requests.post(url, json=payload)
        r = response.json()
        # 将 Base64 转回图片并显示到右侧展示框
        import base64
        import io
        from PIL import Image
        image_data = base64.b64decode(r['images'][0])
        output_img = Image.open(io.BytesIO(image_data))
        
        thought_chain += "【生成管线】像素画面融合完成！"
        return thought_chain, output_img
    except Exception as e:
        return f"连接 SD 后端失败，请确保秋叶启动器已开启 API 模式：{str(e)}", None

# --- Gradio 界面布局 ---
with gr.Blocks(title="EchoPixel - AI 视觉接龙实验室") as demo:
    gr.Markdown("# 🎨 EchoPixel (灵感回响)")
    gr.Markdown("### 基于 AI 视觉接龙的社交交互 Agent —— 连通现实与像素世界")
    
    with gr.Row():
        # 左侧：上传框
        with gr.Column(scale=1):
            gr.Markdown("#### 📸 步骤 1：上传现实瞬间")
            input_i = gr.Image(label="原始照片 (I)", type="pil")
            run_btn = gr.Button("发起视觉接龙", variant="primary")
        
        # 中间：思维链路
        with gr.Column(scale=1):
            gr.Markdown("#### 🧠 步骤 2：Agent 思维链路")
            thought_t = gr.Textbox(label="感知结果 (S) & 剧情续写 (T)", lines=15, interactive=False)
            
        # 右侧：输出框
        with gr.Column(scale=1):
            gr.Markdown("#### 👾 步骤 3：跨次元融合结果")
            output_i = gr.Image(label="像素接龙图 (Iout)")

    # 绑定交互逻辑
    run_btn.click(
        fn=echo_pixel_pipeline,
        inputs=[input_i],
        outputs=[thought_t, output_i]
    )

# 启动程序
if __name__ == "__main__":
    # 强制指定本地 IP，并开启分享链接（可选）
    demo.launch(server_name="127.0.0.1", show_error=True)