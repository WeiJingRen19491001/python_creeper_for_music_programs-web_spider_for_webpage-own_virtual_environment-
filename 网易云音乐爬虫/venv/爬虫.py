import requests
import jieba
from bs4 import BeautifulSoup
from snownlp import SnowNLP
import matplotlib.pyplot as plt
from wordcloud import WordCloud


# 1. 爬取网易云音乐的所有歌手信息
def get_all_artists():
    url = 'https://music.163.com/discover/artist/cat?id=1001&initial=0'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://music.163.com/',
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    artist_list = soup.find_all('a', {'class': 'nm nm-icn f-thide s-fc0'})
    #搜索文档树（1）find_all( name , attrs , recursive , text , **kwargs ) find_all() 方法搜索当前tag的所有tag子节点,并判断是否符合过滤器的条件
    artists = []
    for artist in artist_list:
        artist_id = artist['href'].split('=')[-1]
        artist_name = artist.text
        artists.append({'id': artist_id, 'name': artist_name})
    return artists


# 2. 根据爬取到的歌手信息去爬取所有的专辑信息
def get_artist_albums(artist_id):
    url = f'https://music.163.com/artist/album?id={artist_id}&limit=1000'
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
    return albums



# 3. 根据专辑信息爬取所有的歌曲信息
def get_album_songs(album_id):
    url = f'https://music.163.com/album?id={album_id}'
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
    return songs



# 4. 根据歌曲信息爬取其评论条数并将评论存放于本地文件中
def get_song_comments(song_id,):
    url = f'https://music.163.com/api/v1/resource/comments/R_SO_4_{song_id}?limit=100'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://music.163.com/',
    }
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    total_comments = data['total']
    comments = [comment['content'] for comment in data['comments']]

    # 存放评论到本地文件
    with open(f'{song_id}_comments.txt', 'w', encoding='utf-8',) as file:
        for comment in comments:
            f.write(comment + '\n')

    return total_comments


# 5. 根据文件评论绘制词云
def generate_wordcloud(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        comments = f.read()

    # 使用jieba进行分词
    seg_list = jieba.cut(comments)
    word_list = [word for word in seg_list if len(word) > 1]  # 只保留长度大于1的词语

    # 统计词频
    word_freq = {}
    for word in word_list:
        word_freq[word] = word_freq.get(word, 0) + 1

    # 生成词云图
    wordcloud = WordCloud(
        background_color='white',
        width=800,
        height=600,
        font_path='C:\Windows\Fonts\simsun',  # 指定字体文件的路径
        max_words=100,  # 限制显示的词语数量
        prefer_horizontal=0.9,  # 控制词语水平方向的倾斜程度
        random_state=42
    ).generate_from_frequencies(word_freq)

    plt.figure(figsize=(10, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()


# 6. 对评价进行情感分析并可视化
def sentiment_analysis(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        comments = file.readlines()

    sentiments = []
    for comment in comments:
        s = SnowNLP(comment)
        sentiment = s.sentiments
        sentiments.append(sentiment)

    plt.hist(sentiments, bins=20, edgecolor='black')
    plt.xlabel('Sentiment Score')
    plt.ylabel('Frequency')
    plt.title('Sentiment Analysis')
    plt.show()


# 1. 爬取网易云音乐的所有歌手信息
artists = get_all_artists()
print(artists)

# 2. 根据爬取到的歌手信息去爬取所有的专辑信息
albums = []
for artist in artists:
    artist_id = artist['id']
    artist_albums = get_artist_albums(artist_id)
    albums.extend(artist_albums)
    print(albums)

# 3. 根据专辑信息爬取所有的歌曲信息
songs = []
for album in albums:
    album_id = album['id']
    album_songs = get_album_songs(album_id)
    songs.extend(album_songs)
    print(songs)

# 4. 根据歌曲信息爬取其评论条数并将评论存放于本地文件中
for song in songs:
    song_id = song['id']
    comment_count = get_song_comments(song_id)

# 5. 根据文件评论绘制词云
filename = 'comments.txt'      #需要时输入相应的文件名即可，下同,主要是为了事后分析
generate_wordcloud(filename)

# 6. 对评价进行情感分析并可视化
sentiment_analysis(filename)


