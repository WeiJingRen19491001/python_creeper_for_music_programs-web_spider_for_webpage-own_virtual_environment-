import requests
import jieba
from bs4 import BeautifulSoup
from snownlp import SnowNLP
import matplotlib.pyplot as plt
from wordcloud import WordCloud





with open('jiangnan.txt', 'r', encoding='utf-8') as file:
    comments = file.readlines()

sentiments = []
for comment in comments:
    s = SnowNLP(comment)
    sentiment = s.sentiments
    sentiments.append(sentiment)

plt.hist(sentiments, bins=20, edgecolor='black')
plt.xlabel('情绪得分')
plt.ylabel('频率')
plt.title('情绪分析')
plt.show()