import requests
from bs4 import BeautifulSoup
from snownlp import SnowNLP
import matplotlib.pyplot as plt
from wordcloud import WordCloud

url = 'https://music.163.com/album?id=10786'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Referer': 'https://music.163.com/',
}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')
song_list = soup.find('ul', {'class': 'f-hide'}).find_all('li')
songs = []
for song in song_list:
    song_id = song.find('a')['href'].split('=')[-1]
    song_name = song.find('a').text
    songs.append({'id': song_id, 'name': song_name})

print(songs)