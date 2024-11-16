import requests
from bs4 import BeautifulSoup

url = 'https://comment.bilibili.com/186803402.xml'
response = requests.get(url)
xml = response.text

soup = BeautifulSoup(xml, 'html.parser')
result = [d_tag.text for d_tag in soup.find_all('d')]

# 输出结果
for text in result:
    print(text)