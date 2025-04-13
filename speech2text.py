import os
import json
from groq import Groq
import dotenv
from utils import record_audio_with_silence_detection

dotenv.load_dotenv()

# Initialize the Groq client
client = Groq(api_key=os.getenv("groq_api_key"))


def s2t(filename="../downloads/audio-20250413014718.mp3"):
    # Specify the path to the audio file
    # filename = "../downloads/audio-20250413014718.mp3" # Replace with your audio file!

    # Open the audio file
    with open(filename, "rb") as file:
        # Create a transcription of the audio file
        transcription = client.audio.transcriptions.create(
        file=file, # Required audio file
        model="whisper-large-v3", # Required model to use for transcription
        prompt="Specify context or spelling",  # Optional
        response_format="verbose_json",  # Optional
        timestamp_granularities = ["word", "segment"], # Optional (must set response_format to "json" to use and can specify "word", "segment" (default), or both)
        language="en",  # Optional
        temperature=0.0  # Optional
        )
        transcription_text = transcription.text
        # To print only the transcription text, you'd use print(transcription.text) (here we're printing the entire transcription object to access timestamps)
        print(transcription_text)
        return transcription_text

if __name__ == "__main__":
    # 列出所有音频设备
    # devices = list_audio_devices()
    
    # # 让用户选择录音设备
    # device_id = None
    # while True:
    #     try:
    #         device_id = int(input("\n请选择要使用的录音设备ID（直接回车使用默认设备）: ").strip() or -1)
    #         if device_id == -1:
    #             device_id = None
    #             break
    #         if 0 <= device_id < len(devices):
    #             break
    #         print("无效的设备ID，请重新选择")
    #     except ValueError:
    #         print("请输入有效的数字")
    
    device_id = 0
    
    # 使用新的录音函数
    audio_file, duration = record_audio_with_silence_detection(
        duration=30,  # 最大录音时长30秒
        silence_threshold=3,  # 相对于基准噪音的倍数
        silence_duration=3,  # 2秒静音后停止
        device=device_id
    )
    
    # 转录音频
    transcription = s2t(audio_file)
    print("转录结果:", transcription)