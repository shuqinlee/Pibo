# 适合Pi的ChatBot
## 测试
- speech2text
- text2speech(tts): done, 通过playwright
- text2text
- 唤醒
- 打断
## 用法
- terminal: `chromium-browser --remote-debugging-port=9222`
- 打开网页：https://hailuoai.com/audio
- 打开trojan: `./trojan -c config.json`
- 此处运行 `no_proxy=localhost,127.0.0.1 proxychains python voice_chat.py`

### speech2text
- https://hailuoai.com/audio: 网页调用免费，但API要钱看起来很贵


### 问题

好奇怪，还会播放之前的audio