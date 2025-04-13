import os
import json
from speech2text import s2t
from text2text import t2t
from utils import record_audio_with_silence_detection, ding, dong
import subprocess
import time
import threading
from queue import Queue
import pygame
import traceback
import ipdb

class Config:
    model = "llama-3.3-70b-versatile"
    max_turns = -1
    device_id = 0
    duration = 30
    silence_threshold = 3
    silence_duration = 3
    save_dir = "downloads"


# 初始化 pygame mixer
pygame.mixer.init()

def play_audio(audio_path, volume=1.0):
    """
    播放音频文件并等待播放完成
    """
    try:
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play()
        # 等待音频播放完成
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except Exception as e:
        print(f"播放音频时发生错误: {e}")
    finally:
        pygame.mixer.music.unload()

def t2s(message, last_url=''):
    clean_env = os.environ.copy()
    clean_env.pop("LD_PRELOAD", None)

    result = subprocess.run(
        ["python3", "t2s_worker.py", message, Config.save_dir],
        capture_output=True,
        text=True,
        env=clean_env
    )

    if result.returncode != 0:
        raise RuntimeError("t2s_worker 执行失败：" + result.stderr)
    try:
        print(result.stdout)
        data = json.loads(result.stdout.strip())
        return data["audio_url"], data["audio_path"]
    except Exception as e:
        print(f"发生错误: {e}")
        print(traceback.format_exc())
        return None, None

def voice_chat(device_id=Config.device_id, max_turns=Config.max_turns):
    """
    进行语音对话
    :param device_id: 录音设备ID
    :param max_turns: 最大对话轮数
    """
    print("开始语音对话...")
    print("按Ctrl+C结束对话")
    
    conversation_history = []
    if max_turns == -1:
        max_turns = 1000
    try:
        for turn in range(max_turns):
            print(f"\n--- 第 {turn+1} 轮对话 ---")
            
            # 录制用户语音
            if turn == 0:
                time.sleep(2)
            ding()
            time.sleep(1)
            audio_file, duration = record_audio_with_silence_detection(
                duration=Config.duration,
                silence_threshold=Config.silence_threshold,
                silence_duration=Config.silence_duration,
                device=device_id,
                debug=True
            )
            dong()
            
            # 识别语音
            user_text = s2t(audio_file)
            if not user_text.strip():
                print("未能识别到语音，请重试")
                continue
            
            # 添加到对话历史
            conversation_history.append({"role": "user", "content": user_text})
            
            # 生成回复
            print("\n正在生成回复...")
            assistant_text = t2t(conversation_history, user_text)
            print('assistant_text', assistant_text)
            
            # 添加到对话历史
            conversation_history.append({"role": "assistant", "content": assistant_text})
            
            # 转换为语音并播放
            last_url = ''
            try:
                audio_url, response_audio = t2s(assistant_text)
                if response_audio and last_url != audio_url:
                    print("\n开始播放回复...")
                    play_audio(response_audio)
                    print("音频播放完成")
                    last_url = audio_url
            except Exception as e:
                # 忽略错误
                print(f"发生错误: {e}")
                print(traceback.format_exc())
            
            # 清理临时文件
            try:
                os.remove(audio_file)
                if response_audio:
                    os.remove(response_audio)
            except Exception as e:
                print(f"发生错误: {e}")
                print(traceback.format_exc())
            
            print("\n对话完成，准备下一轮...")
    
    except KeyboardInterrupt:
        print("\n对话已结束")
        pygame.mixer.quit()
    except Exception as e:
        print(f"发生错误: {e}")
        pygame.mixer.quit()

if __name__ == "__main__":
    voice_chat() 
    # audio_url, audio_path = t2s("你好，我是小明，很高兴认识你")
    # print(audio_url, audio_path)
    # play_audio(audio_path)