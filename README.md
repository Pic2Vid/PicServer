# Pic2Vid: Image-to-Video Generation System

## 1. 项目简介

**Pic2Vid** 是一个基于 **WAN 2.1 扩散模型**的图像生成视频系统。  
用户可以通过上传一张图片并输入文本描述（Prompt），生成连贯的视频序列。  
系统使用 **ComfyUI** 作为可视化流程调度平台，支持快速调整参数和生成控制。

本项目作为课程实验展示。

---

## 2. 功能特点

- 支持 **图片 + 文本条件**生成视频
- 自动处理视频帧连续性，保证动作连贯
- 可通过 ComfyUI 可视化界面调节生成参数
- 轻量化支持低显存设备运行
- 支持输出 MP4 视频

---

## 3. 系统结构

```text
用户输入图片 + 文本
        ↓
前端提交生成请求
        ↓
后端构建 ComfyUI Workflow
        ↓
ComfyUI 调度模型推理
        ↓
T5 文本编码 → WAN 2.1 视频扩散生成 → VAE 解码
        ↓
生成视频文件 (MP4)
        ↓
前端展示
```

## 4. 环境依赖

- Python >= 3.10
- PyTorch >= 2.x
- CUDA >= 11.8（可选 GPU 加速）
- ComfyUI（请克隆官方版本或本项目支持版本）
- 其他依赖;

克隆ComfyUI 示例
```bash
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI
# 根据官方指南安装依赖
```
## 5. 所需模型

| 模型 | 说明 | 使用位置 |
|------|------|----------|
| WAN 2.1 | 核心视频扩散生成模型 | ComfyUI Workflow |
| T5 Text Encoder | 文本 Prompt 编码 | ComfyUI Workflow |
| VAE Decoder | 潜空间视频解码为真实视频 | ComfyUI Workflow |

> **提示**：模型权重请自行下载或放置在 `models/` 目录下。

## 6. 使用方法

1. **克隆本项目**：

```bash
git clone https://github.com/YourName/Pic2Vid.git
cd Pic2Vid
```
2.**准备 ComfyUI 与模型权重（见上节）**

3.**运行后端服务**
```python
python main.py
```

4.**前端操作**


- 打开前端页面
- 上传图片并输入文本描述
- 点击生成视频

5.**查看生成结果**
视频生成完成后，可在 output/ 文件夹中和前端查看 MP4 文件

