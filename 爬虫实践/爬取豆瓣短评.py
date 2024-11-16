# 使用import导入requests模块
import requests

# 从bs4中导入BeautifulSoup
from bs4 import BeautifulSoup

# 使用import导入jieba模块
import jieba

# 从pyecharts.charts中导入WordCloud模块
from pyecharts.charts import WordCloud

# 将豆瓣电影评论URL地址，赋值给变量url
url = "https://movie.douban.com/subject/2129039/comments?sort=new_score&status=P"

# 将User-Agent以字典键对形式赋值给headers
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"}

# 将 url 和 headers参数，添加进requests.get()中，将字典headers传递headers参数，给赋值给response
response = requests.get(url, headers=headers)

# 将服务器响应内容转换为字符串形式，赋值给html
html = response.text

# 使用BeautifulSoup()传入变量html和解析器lxml，赋值给soup
soup = BeautifulSoup(html, "lxml")

# 使用find_all()查询soup中class="short"的节点，赋值给content_all
content_all = soup.find_all(class_="short")

# 创建一个空白列表wordList
wordList = []

# for循环遍历content_all
for content in content_all:

    # 获取每个节点中标签内容，赋值给contentString
    contentString = content.string

    # 使用jieba.lcut()将contentString进行分词，赋值给words
    words = jieba.lcut(contentString)

    # 将列表wordList和列表words进行累加
    wordList = wordList + words

# 创建一个空白字典wordDict
wordDict = {}

# TODO for循环遍历列表wordList
for word in wordList:
        # 判断为这几个词语时
    if word == ".." or word == "......":
        # 继续下次循环
        continue

    # TODO 如果列表中的元素长度大于1
    if len(word) > 1:
        # TODO 如果该元素不存在字典的键中
        if word not in wordDict.keys():
            # TODO 将字典中键所对应的值设置为1
            wordDict[word] = 1
        # TODO 否则
        else:
            # TODO 将字典中键所对应的值累加
            wordDict[word] += 1
# TODO 创建WordCloud对象，赋值给wordCloud
wordCloud = WordCloud()
# TODO 使用add()函数，series_name的值设置为空
# data_pair的值为字典wordDict转换成由元组组成的列表；
# 将word_size_range的值设置为[20,80]。
wordCloud.add(series_name="", data_pair = wordDict.items(), word_size_range = [20,80])

# TODO 使用wordCloud.render()存储文件，设置文件名为wordcloud.html
wordCloud.render('wordcloud.html')

# TODO 使用print输出 success
print('success')