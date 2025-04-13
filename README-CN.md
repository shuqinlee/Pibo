# Pibo - 小而妙的语音伙伴 🤖

**Pibo** 是一个极简的语音助手实验项目，面向好奇的极客、独立开发者，以及所有希望以自己的方式与计算机对话的人。无需付费、无需云服务、没有黑盒——只依靠完全免费的开源工具，打造实时、自然的语音交互体验。项目总成本：**￥0**。

最初为树莓派打造，但可以在任何设备上运行。

> English Version: https://github.com/shuqinlee/Pibo/blob/main/README.md.

---

## ✨ 项目亮点

- 🎙️ **实时语音检测**：开口即录，停下来它就知道  
- 🧠 **智能对话系统**：基于 Groq API 与 LLaMA 3.3 70B（或其他兼容模型）  
- 🔊 **高质量语音合成**：通过 Minimax TTS 合成自然流畅的语音  
- 🤫 **静音感知机制**：像朋友一样懂得你在思考或停顿  
- 🧩 **模块化架构**：易于扩展、修改、自由发挥

---

## 🛠️ 技术架构

- **语音识别（STT）**：使用 Groq API 调用 Whisper Large V3（可替换）  
- **对话引擎**：通过 Groq API 接入 LLaMA 3.3 70B（支持其他模型）  
- **语音合成（TTS）**：Playwright 自动控制浏览器调用 Minimax TTS  
- **音频播放**：使用 PyGame 实现低延迟播放反馈

---

## 🚀 快速开始

### 环境依赖

- Python 3.8+
- Chrome 浏览器（用于语音合成）
- 麦克风

### 安装步骤

```bash
git clone https://github.com/shuqinlee/Pibo
cd Pibo
pip install -r requirements.txt
playwright install
```

### 配置环境变量

创建 `.env` 文件，并填入以下内容：

```
groq_api_key=your_groq_api_key
```

### 运行程序

先启动 Chrome 并开启远程调试端口：

```bash
google-chrome --remote-debugging-port=9222
```

然后运行：

```bash
python voice_chat.py
```

💡 小提示：如在中国大陆无法访问 Groq API，可使用 `proxychains` 等代理工具。

启动后：

- 听到提示音即表示可以说话
- Pibo 会自动检测您的语音输入
- 停止说话后，它会自动回复
- 按下 `Ctrl+C` 结束程序

---

## 🔧 高级配置

可以在 `Config` 类中自定义以下参数：

- `model`：对话模型（支持任意 Groq API 提供的模型）
- `max_turns`：最大对话轮数
- `silence_threshold`：静音识别灵敏度
- `silence_duration`：静音等待持续时间（秒）
- `save_dir`：保存音频文件的目录

---

## 🔭 未来计划（not guaranteed）
- 🗣️ **语音唤醒**：支持始终监听模式，添加类似 “Hey Pibo” 的热词唤醒功能，基于轻量级引擎实现，如Porcupine、Snowboy、whisper-tiny
- 💬 **个性化对话**：结合当前时间与历史对话记录，生成定制化内容，让 Pibo 更像一个懂你的伙伴（考虑使用 RAG、向量数据库等技术）  

- 📈 **时延分析**：可视化识别、生成、合成各阶段延迟，用于持续优化响应速度  

- 🌊 **流式语音合成**：替换当前整段式合成为实时流式播放，提升对话流畅度  

- 🌍 **离线模式探索**：为边缘设备提供轻量级离线能力支持  

- 🧪 **多设备适配测试**：优化在 Raspberry Pi Zero、台式机、笔记本等不同硬件上的运行效果

- 语音唤醒

---

## 📄 许可证

MIT License

---

> _“纯好奇心项目。成本￥0，快乐：无价。”_
