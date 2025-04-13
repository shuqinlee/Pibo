from playwright.sync_api import sync_playwright
import time
import requests
import os
import json
import sys
from utils import play_audio

def t2s(message, save_dir="downloads"):
    with sync_playwright() as p:
        # 连接到已开启的浏览器实例
        browser = p.chromium.connect_over_cdp('http://127.0.0.1:9222')
        
        # 获取所有上下文
        contexts = browser.contexts
        # 获取第一个上下文中的所有页面
        pages = contexts[0].pages

        # 选择一个标签页进行操作
        page = pages[0]
        download_link = page.locator('a[href*="cdn.hailuoai.com"]')  # 通过 href 中的部分链接来定位
        last_url = download_link.get_attribute('href')

        textarea = page.locator('textarea')  # 替换为实际的 placeholder 或其他唯一标识符
        textarea.fill(message)

        button = page.locator('button.relative')  # 定位第一个图片中的按钮
        button.click()

        # 等待一段时间，以便查看效果
        page.wait_for_selector('a[href*="cdn.hailuoai.com"]', state="attached")
        while True:
            download_link = page.locator('a[href*="cdn.hailuoai.com"]')  # 通过 href 中的部分链接来定位
            audio_url = download_link.get_attribute('href')
            if audio_url != last_url:
                break
            time.sleep(2)

        # 输出下载链接
        # print(f"音频文件下载链接：{audio_url}")

        # 创建下载目录
        download_dir = save_dir
        os.makedirs(download_dir, exist_ok=True)

        # 下载音频文件
        response = requests.get(audio_url)
        audio_path = os.path.join(download_dir, "audio-" + time.strftime("%Y%m%d%H%M%S") + ".mp3")
        with open(audio_path, "wb") as f:
            f.write(response.content)
        print(json.dumps({"audio_url": audio_url, "audio_path": audio_path}))
        

def t2s_inner(message, q, save_dir="downloads"):
    os.environ.pop("LD_PRELOAD", None)
    with sync_playwright() as p:
        
        browser = p.chromium.connect_over_cdp('http://127.0.0.1:9222')
        
        # 获取所有上下文
        contexts = browser.contexts
        # 获取第一个上下文中的所有页面
        pages = contexts[0].pages

        # 选择一个标签页进行操作
        page = pages[0]

        textarea = page.locator('textarea')  # 替换为实际的 placeholder 或其他唯一标识符
        textarea.fill(message)

        button = page.locator('button.relative')  # 定位第一个图片中的按钮
        button.click()

        # 等待生成按钮状态变化
        # page.wait_for_timeout(5000)
        print("等待语音生成...")
        # 等待按钮中的"生成中"文本消失
        page.wait_for_selector('button.relative:not(:has-text("生成中"))', timeout=30000)
        print("语音生成完成")

        # 确保下载链接已经更新
        page.wait_for_selector('a[href*="cdn.hailuoai.com"]', state="attached")
        download_link = page.locator('a[href*="cdn.hailuoai.com"]')  # 通过 href 中的部分链接来定位
        audio_url = download_link.get_attribute('href')

        # 输出下载链接
        print(f"音频文件下载链接：{audio_url}")

        # 创建下载目录
        download_dir = save_dir
        os.makedirs(download_dir, exist_ok=True)

        # 下载音频文件
        print("当前 LD_PRELOAD:", os.environ.get("LD_PRELOAD"))

        response = requests.get(audio_url, proxies={})
        audio_path = os.path.join(download_dir, "audio-" + time.strftime("%Y%m%d%H%M%S") + ".mp3")
        with open(audio_path, "wb") as f:
            f.write(response.content)
        q.put((audio_url, audio_path))


if __name__ == "__main__":
    msg = sys.argv[1]
    save_dir = sys.argv[2]
    t2s(msg, save_dir)