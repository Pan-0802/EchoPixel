# 生成模块：对接 SD API 执行局部重绘 [cite: 34, 50]

import base64
import requests
import io
from PIL import Image

def encode_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode('utf-8')

def generate_inpainting(original_img_path, mask_img_path, prompt):
    url = "http://127.0.0.1:7860/sdapi/v1/img2img"
    
    # 1. 编码原图 (I) 和 掩码 (M)
    base64_init = encode_image(original_img_path)
    base64_mask = encode_image(mask_img_path)
    
    payload = {
        "prompt": prompt,
        "negative_prompt": "blur, realistic, photo, lowres, watermark",
        # 传入原图 I
        "init_images": [base64_init],
        # 传入掩码 M
        "mask": base64_mask,
        # inpainting_fill: 1 代表使用原图底色作为初始噪声，对应公式中的融合逻辑
        "inpainting_fill": 1,
        "inpaint_full_res": True, # 开启全分辨率局部重绘，保证像素精度
        "inpaint_full_res_padding": 32,
        "steps": 25,
        "cfg_scale": 7,
        "sampler_name": "Euler a",
        
        # 2. 注入 ControlNet 约束 (可选，但方案推荐)
        # 注意：这里要求你安装了 sd-webui-controlnet 插件并开启了 API
        "alwayson_scripts": {
            "controlnet": {
                "args": [
                    {
                        "enabled": True,
                        "module": "canny", # 预处理器
                        "model": "control_v11p_sd15_canny", # 需要你下载这个模型
                        "weight": 0.7, # 约束强度
                        "image": base64_init # 让 ControlNet 从原图提取结构
                    }
                ]
            }
        }
    }

    print("正在计算公式：I_out = (1-M)*I + M*D(z0)...")
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        r = response.json()
        image_data = base64.b64decode(r['images'][0])
        image = Image.open(io.BytesIO(image_data))
        image.save('echo_pixel_output.png')
        image.show()
        print("重绘完成！图片已保存为 'echo_pixel_output.png'")
    else:
        print(f"API 请求失败: {response.text}")

if __name__ == "__main__":
    # 测试执行
    # 你需要准备：
    # 1. test_photo.jpg (真实场景图)
    # 2. test_mask.png (黑底白块图，白色块就是你想画像素小人的位置)
    
    prompt = "pixel art, a cute 8-bit ghost, highly detailed, vibrant colors <lora:你的像素Lora:1>"
    # generate_inpainting("assets/test_photo.jpg", "assets/test_mask.png", prompt)