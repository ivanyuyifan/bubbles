import requests
from bs4 import BeautifulSoup
import os

output_folder = '/Users/fafaya/Desktop/bubbles/爬虫实践/网站爬取的图片'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

url = 'https://nocturne-spider.baicizhan.com/practise/31.html'
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'}

response = requests.get(url, headers=headers)
response.encoding = response.apparent_encoding
html = response.text
soup = BeautifulSoup(html, 'lxml')
content_all = soup.find_all(class_='pic')
count = 0
for content in content_all:
    #这一步是在获取图片的名字，来源为缩略图
    imgContent = content.find('img')
    imgName = imgContent.attrs['alt']
    imgName = imgName.replace(' ', '_')
    
    imgContent1 = content.find('a')
    #这一步是想获取高清图片（之前find('img')找到的是缩略图
    imgUrl = imgContent1.attrs['href']
    imgResponse = requests.get(imgUrl)
    #下一步是获取高清图网页页面的所有内容
    htmlA = imgResponse.text
    soupA = BeautifulSoup(htmlA, 'lxml')
    imgResponseA = soupA.find(style="visibility: visible;width: 100%;").attrs['src']#这里获取的是高清图的source
    imgResponseB = requests.get(imgResponseA)
    img = imgResponseB.content
    
    if imgName != '爱上紫禁城':
        img_path = os.path.join(output_folder, f'{imgName}.jpg')
    else:
        count += 1
        img_path = os.path.join(output_folder, f'{imgName}-{count}.jpg')

    with open(img_path, 'wb') as f:
        f.write(img)
    print(f"图片已保存: {img_path}")
        