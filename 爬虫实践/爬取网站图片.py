# 是时候展示真正的技术啦
import requests
from bs4 import BeautifulSoup

url = 'https://nocturne-spider.baicizhan.com/practise/31.html'
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'}
response = requests.get(url, headers=headers)
response.encoding = response.apparent_encoding
html = response.text
soup = BeautifulSoup(html, 'lxml')
content_all = soup.find_all(class_='pic')
count = 0
for content in content_all:
    imgContent = content.find('img')
    imgName = imgContent.attrs['alt']
    imgName = imgName.replace(' ', '_')
    
    imgContent1 = content.find('a')
    imgUrl = imgContent1.attrs['href']
    imgResponse = requests.get(imgUrl)
    
    htmlA = imgResponse.text
    soupA = BeautifulSoup(htmlA, 'lxml')
    imgResponseA = soupA.find('img').attrs['src']
    imgResponseB = requests.get(imgResponseA)
    img = imgResponseB.content
    
    if imgName != '爱上紫禁城':
        with open(f'{imgName}.jpg', 'wb') as f:
            f.write(img)
    else:
        count += 1
        with open(f'{imgName}-{count}.jpg', 'wb') as f:
            f.write(img)
        