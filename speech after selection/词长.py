import nltk
import pandas as pd
import os
import matplotlib.pyplot as plt

punctuation =  r"""!"#$%&'’()*+,-./:;<=>?@[\]^_`{|}~"""
wordlength_result = []

def file_read(filepath):
    file = open(filepath, 'r', encoding='utf-8')
    content = file.read()

    return content

folder_path = '/Users/fafaya/Desktop/bubbles/speech after selection'


for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):
        filepath = os.path.join(folder_path, filename)
        speech_content = file_read(filepath)

        words = nltk.word_tokenize(speech_content)
        word_length = {}
        total_num = 0
        for w in words:
            if w not in punctuation:
                total_num += 1
                length = len(list(w))
                word_length[length] = word_length.get(length, 0) + 1

        word_length_sorted = dict(sorted(word_length.items(), key=lambda x:x[1]))

        word_len_distribution = {}#词长字典
        for k, v in word_length_sorted.items():
            word_len_distribution[k] = v / total_num

        metrics = {
            '演讲名称' : filename,
            '总词数': total_num,
            '词长统计': word_length_sorted,
            '词长分布': word_len_distribution
                   }
        
        wordlength_result.append(metrics)
  
wordlength_result = pd.DataFrame(wordlength_result)
import matplotlib.pyplot as plt

# 绘制每篇演讲的词长分布
def plot_word_length_distribution(wordlength_result):
    plt.figure(figsize=(14, 8))  # 设置图像大小
    plt.xticks(fontsize=12)  # 设置横坐标字体大小
    plt.yticks(fontsize=12)  # 设置纵坐标字体大小
    colors = ['r', 'b', 'g', 'k', 'y', 'm', 'c']  # 定义多种颜色，反复使用
    
    # 遍历每篇演讲数据，绘制词长分布
    for i, metrics in enumerate(wordlength_result):
        word_len_distribution = metrics['词长分布']
        
        # 对词长分布字典按照词长从小到大排序
        sorted_word_len_distribution = dict(sorted(word_len_distribution.items()))
        
        # 提取排序后的词长和对应的分布比例
        word_lengths = list(sorted_word_len_distribution.keys())
        distribution_values = list(sorted_word_len_distribution.values())
        
        # 绘制折线图
        plt.plot(word_lengths, distribution_values, color=colors[i % len(colors)], 
                 linewidth=2, linestyle='-', label=metrics['演讲名称'])
        
        # 在折线图上方显示每个点的分布比例值
        for x, y in zip(word_lengths, distribution_values):
            plt.text(x, y, f'{y:.2f}', ha='right', va='bottom', fontsize=10)

    # 设置图表标题和标签
    plt.title('Speech Word Length Distribution', fontsize=16)  # 设置标题
    plt.xlabel('Word Length', fontsize=14)  # 设置横坐标标签
    plt.ylabel('Frequency Rate', fontsize=14)  # 设置纵坐标标签
    plt.grid(True)  # 显示网格
    plt.legend(loc='upper right', fontsize=10)  # 在右上角显示图例

    # 设置横坐标为整数
    plt.xticks(ticks=word_lengths)  # 直接将刻度设置为整数的词长列表
    
    # 保存图像
    plt.savefig('/Users/fafaya/Desktop/bubbles/speech after selection/word_length_distribution.png')
    plt.show()

# 调用函数生成词长分布图
plot_word_length_distribution(wordlength_result.to_dict('records'))
wordlength_result.to_excel('speech after selection/wordlength.xlsx', sheet_name='wordlength', index=True)