import pandas as pd
import os
import nltk
import chardet
from matplotlib import pyplot as plt

root = r'/Users/fafaya/Desktop/Paris Olympics/Paris Olympics/奥林匹克英文推文'

# 对每篇文本记录词长频数和词长分布

folderlist = os.listdir(root)

folderlist_temp = []

for folder in folderlist:
    if '.DS_Store' not in folder:
        folderlist_temp.append(folder)

folderlist = folderlist_temp

data = {}  # 记录每一个类别（BBC和CNN）下的所有文件内容

def read_file_with_chardet(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']

    with open(file_path, 'r', encoding=encoding) as f:
        return f.read().strip()


for folder in folderlist:
    papers = {}  # 这是用来记录文件名和里面的内容的字典

    folder_path = os.path.join(root, folder)
    filelist = os.listdir(folder_path)

    filelist_temp = []
    for file in filelist:
        if '.DS_Store' not in file:
            filelist_temp.append(file)

    filelist = filelist_temp

    for file in filelist:
        file_path = os.path.join(folder_path, file)
        content = read_file_with_chardet(file_path)  # 使用chardet自动检测编码
        papers[file] = content

    data[folder] = papers

# 统计词长频数和词长分布
punctuation = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
result_en = []

for press_name, papers in data.items():
    for title, content in papers.items():  # 进入了每篇新闻的内容
        words = nltk.word_tokenize(content)
        word_length = {}  # 记录每一篇文本的词长的字典
        total_num = 0  # 记录总词数
        for w in words:
            if w not in punctuation:
                total_num += 1
                length = len(list(w))
                word_length[length] = word_length.get(length, 0) + 1

        word_length_sorted = dict(sorted(word_length.items(), key=lambda x: x[1], reverse=True))  # 将词长字典按照频数从高至低排序
        word_len_distribution = {}
        for k, v in word_length_sorted.items():
            word_len_distribution[k] = v / total_num

        metrics = {
            '题目': title,
            '新闻出版社': press_name,
            '总词数': total_num,
            '词长统计': word_length_sorted,
            '词长分布': word_len_distribution
        }
        result_en.append(metrics)

result_en = pd.DataFrame(result_en)
result_en

# 以不同的新闻出版社作为研究单位，记录每个出版社的词长频数
word_len_class = {}

for press_name, papers in data.items():
    word_len_class_level = {}  # 记录一个出版社类型的整体词长频数
    for title, content in papers.items():
        words = nltk.word_tokenize(content)
        for w in words:
            if w not in punctuation:
                length = len(list(w))
                word_len_class_level[length] = word_len_class_level.get(length, 0) + 1

    word_len_class[press_name] = dict(sorted(word_len_class_level.items(), key=lambda x: x[0], reverse=False))


word_len_class


def line_chart(word_len):
    plt.figure(figsize=(50, 30))  # 图像整体布局
    plt.xticks(fontsize=50)  # 设置横坐标
    plt.yticks(fontsize=50)  # 设置纵坐标
    colors = ['r', 'b', 'g', 'k', 'y']  # 定义六种颜色，反复使用
    # 设置每一个（x，y）坐标，以及折线的颜色和形状
    for i, (cls, data) in enumerate(word_len.items()):
        x1 = list(data.keys())
        y1 = [round(value / sum(list(data.values())), 4) for value in list(data.values())]
        plt.plot(x1, y1, color=colors[i % len(colors)], linewidth=4, linestyle='-')
        for x, y in zip(x1, y1):
            plt.text(x, y, f'{y}', ha='left', va='bottom', fontsize=30)
    plt.title('Word Length Distribution Map', fontsize=50)  # 设置图像标题
    plt.xlabel('Word Length', fontsize=50)  # 设置横坐标内容
    plt.ylabel('Rate', fontsize=50)  # 设置纵坐标内容
    plt.grid(True)  # 用网格形式展示
    plt.legend(list(word_len.keys()), loc='upper right', fontsize=50)  # 在图像右上角设置折线的对应关系
    # 设置横坐标以1个单位间隔，因为词长通常是1，2，3...
    ax = plt.gca()
    x_major_locator = plt.MultipleLocator(1)
    ax.xaxis.set_major_locator(x_major_locator)
    # 保存词长图像
    plt.savefig(r'/Users/fafaya/Desktop/Paris Olympics/Paris Olympics/奥林匹克英文推文英文词长分布.png')
    # 在结果框中展示图像
    plt.show()


line_chart(word_len_class)  # 对上一步获得的各类讲演类型词长频数字典调用绘制折线图的函数

print(result_en)
word_len_class = pd.DataFrame(word_len_class)
print(word_len_class)
result_en.to_excel('result_en.xlsx', index=False)
word_len_class.to_excel('word_len_class.xlsx', index=False)