import requests
import base64
import io
from PIL import Image

# 1. 设置 API 地址（本地 SD 默认地址）
url = "http://127.0.0.1:7860/sdapi/v1/txt2img"

# 2. 定义符合 EchoPixel 方案的像素风 Payload [cite: 30, 50]
payload = {
    "prompt": "pixel art, a cute robot studying in a futuristic library, vibrant colors, 8-bit style",
    "negative_prompt": "blur, photo, realistic, low quality",
    "steps": 20,
    "width": 512,
    "height": 512,
    "cfg_scale": 7,
    "sampler_name": "Euler a",
    # 强制注入方案要求的像素风格约束 [cite: 50]
    "override_settings": {
        "sd_model_checkpoint": "sd1.5_anything-v5.safetensors" 
    }
}

print("正在向 EchoPixel 后端请求生成像素画面...")

# 3. 发送 POST 请求 [cite: 44, 64]
response = requests.post(url, json=payload)

if response.status_code == 200:
    r = response.json()
    # 4. 解析返回的 Base64 图像数据
    image_data = base64.b64decode(r['images'][0])
    image = Image.open(io.BytesIO(image_data))
    
    # 5. 保存并展示结果
    image.save('first_echo_pixel.png')
    image.show()
    print("生成成功！图片已保存为 'first_echo_pixel.png'")
else:
    print(f"请求失败，错误代码: {response.status_code}")