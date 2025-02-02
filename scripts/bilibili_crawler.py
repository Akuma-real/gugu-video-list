import requests
import json
import os
from datetime import datetime

# UP主配置信息
UP_CONFIG = {
    'uid': '3546719115545125',
    'name': 'Double咕Gu'
}

def get_up_videos(uid):
    print(f"开始获取UP主 {UP_CONFIG['name']} (UID: {uid}) 的视频信息...")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    url = f'https://api.bilibili.com/x/space/arc/search?mid={uid}&ps=30&tid=0&pn=1&order=pubdate'
    print(f"请求URL: {url}")
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        print(f"API响应状态码: {data['code']}")
        
        if data['code'] == 0:
            videos = data['data']['list']['vlist']
            if videos:
                video = videos[0]
                print(f"成功获取到最新视频: {video['title']}")
                return {
                    'title': video['title'],
                    'cover': video['pic'],
                    'url': f"https://www.bilibili.com/video/{video['bvid']}",
                    'publish_time': video['created']
                }
            else:
                print("未找到任何视频")
        else:
            print(f"API返回错误: {data.get('message', '未知错误')}")
    except Exception as e:
        print(f"发生错误: {e}")
    return None

def main():
    print("开始执行爬虫脚本...")
    
    # 创建数据目录
    os.makedirs('data', exist_ok=True)
    print("数据目录已创建/确认")
    
    # 获取最新视频信息
    latest_video = get_up_videos(UP_CONFIG['uid'])
    
    if latest_video:
        output_file = "data/latest_video.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json_data = {
                'up_name': UP_CONFIG['name'],
                'uid': UP_CONFIG['uid'],
                'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'video': latest_video
            }
            json.dump(json_data, f, ensure_ascii=False, indent=2)
            print(f"数据已保存到 {output_file}")
            print("保存的数据内容:")
            print(json.dumps(json_data, ensure_ascii=False, indent=2))
    else:
        print("未能获取视频信息，退出程序")

if __name__ == '__main__':
    main() 