import requests
from bs4 import BeautifulSoup
from snownlp import SnowNLP
import matplotlib.pyplot as plt
from wordcloud import WordCloud



# 2. 根据爬取到的歌手信息去爬取所有的专辑信息

url = 'https://music.163.com/artist/album?id=3684&limit=1000'
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://music.163.com/',
    }
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')
album_list = soup.find_all('a', {'class': 'tit s-fc0'})
albums = []
for album in album_list:
        album_id = album['href'].split('=')[-1]
        album_name = album.text.strip()
        albums.append({'id': album_id, 'name': album_name})



print(albums)