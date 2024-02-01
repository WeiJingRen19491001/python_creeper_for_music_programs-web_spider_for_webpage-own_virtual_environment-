import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud

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


# 示例使用：
filename = 'jiangnan.txt'
generate_wordcloud(filename)
