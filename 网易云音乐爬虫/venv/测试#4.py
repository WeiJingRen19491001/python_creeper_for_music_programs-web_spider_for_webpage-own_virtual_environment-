import requests
import json

# 4. 根据歌曲信息爬取其评论条数并将评论存放于本地文件中

url = f'https://music.163.com/api/v1/resource/comments/R_SO_4_108779?limit=100'
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://music.163.com/',
    }
response = requests.get(url, headers=headers)
data = json.loads(response.text)
total_comments = data['total']
comments = [comment['content'] for comment in data['comments']]
print(comments)
print(total_comments)


with open('jiangnan.txt', 'w', encoding='utf-8') as f:
        for comment in comments:
            f.write(comment + '\n')


