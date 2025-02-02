import requests
import json
import os
from datetime import datetime

def get_up_videos(uid):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    url = f'https://api.bilibili.com/x/space/arc/search?mid={uid}&ps=30&tid=0&pn=1&order=pubdate'
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        
        if data['code'] == 0:
            videos = data['data']['list']['vlist']
            # 只返回最新的一个视频信息
            if videos:
                video = videos[0]
                return {
                    'title': video['title'],
                    'cover': video['pic'],
                    'url': f"https://www.bilibili.com/video/{video['bvid']}",
                    'publish_time': video['created']
                }
    except Exception as e:
        print(f"Error fetching data: {e}")
    return None

def main():
    # 从环境变量获取UP主信息
    uid = os.environ['UP_UID']
    up_name = os.environ['UP_NAME']
    
    # 创建数据目录
    os.makedirs('data', exist_ok=True)
    
    # 获取最新视频信息
    latest_video = get_up_videos(uid)
    
    if latest_video:
        output_file = "data/latest_video.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                'up_name': up_name,
                'uid': uid,
                'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'video': latest_video
            }, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main() 