import numpy as np
import sounddevice as sd
from pydub import AudioSegment

import soundfile as sf
import numpy as np
from datetime import datetime
import time as time_module
from collections import deque
import os

def play_audio(audio_path, volume=1.0):
    try:
        # 使用 pydub 加载音频文件
        audio = AudioSegment.from_file(audio_path)
        
        # 转换为 numpy 数组
        samples = np.array(audio.get_array_of_samples())
        
        # 调整音量
        samples = (samples * volume).astype(np.int16)
        
        # 播放音频
        sd.play(samples, audio.frame_rate)
        sd.wait()
    except Exception as e:
        print(f"播放音频时发生错误: {e}")

def ding():
    audio_path = "./sound/ding.wav"
    play_audio(audio_path)

def dong():
    audio_path = "./sound/dong.wav"
    play_audio(audio_path)


def list_audio_devices():
    """列出所有可用的音频设备"""
    devices = sd.query_devices()
    print("\n可用的音频设备：")
    for i, device in enumerate(devices):
        print(f"{i}: {device['name']} (输入通道: {device['max_input_channels']}, 输出通道: {device['max_output_channels']})")
        if device['max_input_channels'] > 0:  # 如果是输入设备
            print(f"   支持的采样率: {device['default_samplerate']}Hz")
    return devices

def get_device_samplerate(device_id):
    """获取设备支持的采样率"""
    device_info = sd.query_devices(device_id)
    return int(device_info['default_samplerate'])

def audio_callback(indata, frames, time, status):
    """音频回调函数，用于检测声音"""
    if status:
        print(status)
    # 计算音频数据的能量
    volume_norm = np.linalg.norm(indata) * 10
    audio_callback.volume = volume_norm

def record_audio_with_silence_detection(duration=30, silence_threshold=0.1, silence_duration=2, device=None, save_dir="downloads", debug=False):
    """
    录制音频，当检测到指定时长的静音时自动停止
    :param duration: 最大录音时长（秒）
    :param silence_threshold: 静音阈值（相对于基准噪音的倍数）
    :param silence_duration: 静音持续多少秒后停止（秒）
    :param device: 设备ID，如果为None则使用默认设备
    :return: (保存的文件路径, 实际录音时长)
    """
    # 获取设备支持的采样率
    sample_rate = get_device_samplerate(device) if device is not None else 44100
    
    # 确保下载目录存在
    os.makedirs(save_dir, exist_ok=True)
    
    # 生成文件名
    filename = os.path.join(save_dir, f"audio-{datetime.now().strftime('%Y%m%d%H%M%S')}.wav")
    
    if debug:
        print(f"开始录音，最大持续 {duration} 秒...")
        print(f"使用采样率: {sample_rate}Hz")
        print(f"静音检测阈值: {silence_threshold}")
        print(f"静音持续 {silence_duration} 秒后自动停止")
    
    # 初始化录音数据
    audio_data = []
    start_time = time_module.time()
    last_sound_time = start_time
    
    # 用于存储最近的音频能量值
    energy_buffer = deque(maxlen=50)
    baseline_noise = None
    calibration_time = 1.0  # 校准时间（秒）
    calibration_complete = False
    
    def calculate_energy(data):
        """计算音频数据的能量"""
        # 使用RMS（均方根）计算能量
        return np.sqrt(np.mean(data**2))
    
    def callback(indata, frames, time_info, status):
        if status:
            print(status)
        
        # 增加音量增益
        amplified_data = indata * 5  # 增加5倍音量
        
        # 保存音频数据
        audio_data.append(amplified_data.copy())
        
        # 计算当前帧的能量
        current_energy = calculate_energy(amplified_data)
        energy_buffer.append(current_energy)
        
        nonlocal baseline_noise, calibration_complete, last_sound_time
        
        # 校准阶段：收集环境噪音基准
        if not calibration_complete:
            if time_module.time() - start_time >= calibration_time:
                baseline_noise = np.mean(list(energy_buffer))
                calibration_complete = True
                if debug:
                    print(f"噪音基准校准完成: {baseline_noise:.2f}")
        else:
            # 计算相对于基准噪音的能量比
            relative_energy = current_energy / baseline_noise if baseline_noise > 0 else 0
            
            # 调试信息
            if debug and len(energy_buffer) % 1000 == 0:  # 每10帧打印一次
                print(f"当前能量: {current_energy:.2f}, 相对能量: {relative_energy:.2f}")
            
            # 检测是否有声音
            if relative_energy > silence_threshold:
                last_sound_time = time_module.time()
                print(f"检测到声音，当前能量: {current_energy:.2f}, 相对能量: {relative_energy:.2f}, 时间: {last_sound_time}")
    
    # 开始录音
    with sd.InputStream(samplerate=sample_rate,
                       channels=1,
                       dtype=np.float32,  # 使用浮点数格式以支持更大的动态范围
                       device=device,
                       callback=callback):
        while True:
            current_time = time_module.time()
            elapsed_time = current_time - start_time
            
            # 等待校准完成
            if not calibration_complete:
                time_module.sleep(0.1)
                continue
            
            # 检查是否超过最大录音时长
            if elapsed_time >= duration:
                if debug:
                    print("达到最大录音时长，停止录音")
                break
            
            # 检查是否持续静音
            if current_time - last_sound_time >= silence_duration:
                if debug:
                    print("检测到持续静音，停止录音")
                break
            
            time_module.sleep(0.1)
    
    # 合并录音数据
    recording = np.concatenate(audio_data, axis=0)
    
    # 确保音频数据在有效范围内
    recording = np.clip(recording, -1.0, 1.0)
    
    # 转换为16位整数
    recording = (recording * 32767).astype(np.int16)
    
    actual_duration = len(recording) / sample_rate
    
    # 保存为WAV文件
    sf.write(filename, recording, sample_rate)
    if debug:
        print(f"录音完成！实际录音时长: {actual_duration:.2f}秒")
        print(f"音频已保存到: {filename}")
    
    return filename, actual_duration

def record_audio(duration=5, device=None):
    """
    录制音频
    :param duration: 录音时长（秒）
    :param device: 设备ID，如果为None则使用默认设备
    :return: 保存的文件路径
    """
    # 获取设备支持的采样率
    sample_rate = get_device_samplerate(device) if device is not None else 44100
    
    # 确保下载目录存在
    os.makedirs("../downloads", exist_ok=True)
    
    # 生成文件名
    filename = f"../downloads/audio-{datetime.now().strftime('%Y%m%d%H%M%S')}.wav"
    
    print(f"开始录音，持续 {duration} 秒...")
    print(f"使用采样率: {sample_rate}Hz")
    
    # 录制音频
    recording = sd.rec(int(duration * sample_rate),
                      samplerate=sample_rate,
                      channels=1,
                      dtype=np.int16,
                      device=device)
    sd.wait()  # 等待录音完成
    print("录音完成！")
    
    # 保存为WAV文件
    sf.write(filename, recording, sample_rate)
    print(f"音频已保存到: {filename}")
    
    return filename

if __name__ == "__main__":
    record_audio_with_silence_detection(duration=30, silence_threshold=3, silence_duration=3, device=None, save_dir="downloads", debug=True)