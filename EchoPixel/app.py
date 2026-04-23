import gradio as gr
import requests
import base64
import io
import os
from PIL import Image
from dotenv import load_dotenv
from openai import OpenAI

# 1. 环境初始化
load_dotenv()
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

def get_image_perception(image_path, history_text):
    """
    视觉感知核心：让 Qwen-VL 读取图片并结合历史生成双语描述
    """
    with open(image_path, "rb") as f:
        base64_image = base64.b64encode(f.read()).decode("utf-8")

    # 构造强约束指令
    system_prompt = f"""你是一个像素艺术故事策划。
【当前记忆库】：{history_text if history_text else "故事刚刚开始。"}

【任务】：
1. 观察新图片。
2. 延续记忆库中的剧情，构思这一幕发生的变化。
3. 严格按此格式回复：
剧情描述：[此处写20字内中文]
英文提示词：[此处写一段英文绘图标签]"""

    response = client.chat.completions.create(
        model="qwen-vl-plus",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": system_prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ],
            }
        ],
    )
    return response.choices[0].message.content

# 2. 核心业务流水线
def echo_pixel_pipeline(input_img, history):
    if input_img is None:
        return history, "请先上传一张照片...", None

    # A. 预处理
    temp_input = "input_cache.png"
    input_img.save(temp_input)
    
    # B. 动态感知与记忆联动
    try:
        raw_res = get_image_perception(temp_input, history)
        
        # 解析双语输出
        if "英文提示词：" in raw_res:
            ch_desc = raw_res.split("英文提示词：")[0].replace("剧情描述：", "").strip()
            en_prompt = raw_res.split("英文提示词：")[1].strip()
        else:
            # 保底逻辑：如果 AI 没按格式输出
            ch_desc = "发现新线索"
            en_prompt = raw_res

        # 更新全局记忆
        new_history = history + f"\n- {ch_desc}"
        
        # 构造思维链路显示
        thought_chain = f"📝 历史剧情回顾：\n{history if history else '暂无'}\n"
        thought_chain += f"------------------------\n"
        thought_chain += f"🧠 这一刻发生的：{ch_desc}\n"
        thought_chain += f"✨ 转化为像素指令：{en_prompt}"
        
    except Exception as e:
        print(f"感知引擎报错: {e}")
        return history, f"感知引擎罢工了: {str(e)}", None

    # C. 调用 Stable Diffusion (使用 Qwen 提供的英文提示词)
    style_boost = "(pixel art:1.5), (8-bit:1.2), isometric, retro game style"
    final_prompt = f"{style_boost}, {en_prompt}, <lora:Pony6.sakuemonq.10:1>"
    
    url = "http://127.0.0.1:7860/sdapi/v1/txt2img"
    payload = {
        "prompt": final_prompt,
        "negative_prompt": "blur, realistic, photo, text, watermark, (painting:1.5), (low quality:1.4)",
        "steps": 25,
        "width": 512,
        "height": 512,
        "cfg_scale": 7
    }
    
    try:
        response = requests.post(url, json=payload, timeout=60)
        r = response.json()
        image_data = base64.b64decode(r['images'][0])
        output_img = Image.open(io.BytesIO(image_data))
        
        thought_chain += "\n\n✅ 像素画面接龙成功！"
        return new_history, thought_chain, output_img
    except Exception as e:
        # 失败时依然返回旧的 history，防止状态丢失
        return history, f"连接 SD 后端失败：{str(e)}", None

# 3. 界面布局
with gr.Blocks(title="EchoPixel Agent Lab", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🎨 EchoPixel (灵感回响) v2.0")
    gr.Markdown("### 视觉接龙 Agent：现实影像 → 剧情续写 → 像素重生")
    
    # 核心状态：隐藏的剧情笔记本
    history_state = gr.State("")

    with gr.Row():
        with gr.Column(scale=1):
            input_i = gr.Image(label="📸 步骤1：拍摄现实瞬间", type="pil")
            with gr.Row():
                run_btn = gr.Button("🔥 发起视觉接龙", variant="primary")
                clear_btn = gr.Button("🗑️ 重置故事")
        
        with gr.Column(scale=1):
            thought_t = gr.Textbox(label="🧠 步骤2：Agent 剧情分析 (中文)", lines=12)
            
        with gr.Column(scale=1):
            output_i = gr.Image(label="👾 步骤3：跨次元生成结果")

    # 交互绑定
    run_btn.click(
        fn=echo_pixel_pipeline,
        inputs=[input_i, history_state],
        outputs=[history_state, thought_t, output_i]
    )
    
    # 重置按钮逻辑
    clear_btn.click(lambda: ("", "故事已清空，请上传图片开始新篇章...", None), 
                    None, [history_state, thought_t, output_i])

if __name__ == "__main__":
    # 使用 server_port 避免之前的参数报错
    demo.launch(server_name="127.0.0.1", server_port=9999, show_error=True)