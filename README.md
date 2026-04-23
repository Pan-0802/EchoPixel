# 🎨 EchoPixel (灵感回响)

> **基于 AI 视觉接龙的社交交互 Agent —— 连通现实与像素世界**

本项目是 EchoPixel 方案的交互原型实现，通过感知现实图像语义，结合大模型决策，最终利用 Stable Diffusion 绘制像素风格的“接龙”画面。

## 🌟 核心功能
- **视觉感知**：解析上传照片的环境、主体与情感。
- **思维链路展示**：实时输出 Agent 的逻辑推理过程 (Chain of Thought)。
- **跨次元生成**：注入特定的 Pixel-Art LoRA，统一直出高品质像素风格。

## 📸 运行预览
![运行截图](./first_echo_pixel.png) 
*(建议把你那张图书馆机器人的运行截图 改名为 EchoPixel_Demo.jpg 放在根目录，这样 GitHub 就能直接显示图片了)*

## 🚀 快速开始

### 1. 环境准备
确保已安装 Python 3.10.6+，并克隆本项目：
```bash
git clone [https://github.com/你的用户名/EchoPixel.git](https://github.com/你的用户名/EchoPixel.git)
cd EchoPixel
```

### 2.安装依赖
建议在虚拟环境下运行：
```Bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

### 3.配置后端
本项目依赖 Stable Diffusion WebUI 开启 API 模式运行。<br>
端口：http://127.0.0.1:7860<br>
模型要求：需在 models/Lora 下放置 Pony6.sakuemonq.10 等像素 LoRA。<br>

### 4. 启动原型
```Bash
python EchoPixel/app.py
```
访问 http://127.0.0.1:9999 即可开始交互。

# 🛠️ 技术栈
Frontend: Gradio

Backend: Stable Diffusion API (Aki-v4.11.1)

Logic: Python / PIL

### 启动步骤
#### 第一步：启动 Stable Diffusion 后端 (Aki-v4.11.1)
进入文件夹 D:\Aaone\EchoPixel\sd-webui-aki-v4.11.1-cu128。

双击运行 A启动器.exe。

点击右下角的 “一键启动”。

关键点：等待启动器的黑色控制台窗口出现，并显示 Model loaded in XXXs 以及 Running on local URL: http://127.0.0.1:7860。此时后端 API 才算真正准备好。
#### 第二步：启动 VS Code 并激活环境
打开 VS Code，确保左侧文件栏显示的是你的项目根目录 D:\Aaone\EchoPixel。

按 Ctrl + ~ 打开内置终端。

激活你之前创建的虚拟环境：

````PowerShell

.\.venv\Scripts\activate
````
检查：命令行开头是否出现了 (.venv) 字样？
#### 第三步：运行 Gradio 交互界面
在激活了虚拟环境的终端中输入：

````PowerShell

python EchoPixel/app.py
````
等待终端输出 Running on local URL: http://127.0.0.1:9999。

按住 Ctrl 并点击该链接，或者直接在浏览器输入 127.0.0.1:9999。


