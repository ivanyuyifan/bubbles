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

# 绘制每篇演讲的词长分布（比例）和词长统计（频数）折线图
def plot_word_length_distribution_and_frequency(wordlength_result):
    plt.figure(figsize=(14, 8))  # 设置图像大小
    colors = ['r', 'b', 'g', 'k', 'y', 'm', 'c']  # 定义多种颜色，反复使用

    # 绘制词长分布（比例）图
    plt.subplot(2, 1, 1)  # 2行1列子图的第一个
    for i, metrics in enumerate(wordlength_result):
        word_len_distribution = metrics['词长分布']
        # 排序
        sorted_word_len_distribution = dict(sorted(word_len_distribution.items()))
        
        # 数据
        word_lengths = list(sorted_word_len_distribution.keys())
        distribution_values = list(sorted_word_len_distribution.values())
        
        # 折线图
        plt.plot(word_lengths, distribution_values, color=colors[i % len(colors)], 
                 linewidth=2, linestyle='-', label=metrics['演讲名称'])
        
        # 显示比例值
        for x, y in zip(word_lengths, distribution_values):
            plt.text(x, y, f'{y:.2f}', ha='right', va='bottom', fontsize=10)

    plt.title('Speech Word Length Distribution (Proportion)', fontsize=16)
    plt.xlabel('Word Length', fontsize=14)
    plt.ylabel('Frequency Rate', fontsize=14)
    plt.grid(True)
    plt.legend(loc='upper right', fontsize=10)
    plt.xticks(ticks=word_lengths)

    # 绘制词长统计（频数）图
    plt.subplot(2, 1, 2)  # 2行1列子图的第二个
    for i, metrics in enumerate(wordlength_result):
        word_len_statistics = metrics['词长统计']
        # 排序
        sorted_word_len_statistics = dict(sorted(word_len_statistics.items()))
        
        # 数据
        word_lengths = list(sorted_word_len_statistics.keys())
        frequency_values = list(sorted_word_len_statistics.values())
        
        # 折线图
        plt.plot(word_lengths, frequency_values, color=colors[i % len(colors)], 
                 linewidth=2, linestyle='-', label=metrics['演讲名称'])
        
        # 显示频数值
        for x, y in zip(word_lengths, frequency_values):
            plt.text(x, y, f'{y}', ha='right', va='bottom', fontsize=10)

    plt.title('Speech Word Length Frequency', fontsize=16)
    plt.xlabel('Word Length', fontsize=14)
    plt.ylabel('Frequency', fontsize=14)
    plt.grid(True)
    plt.legend(loc='upper right', fontsize=10)
    plt.xticks(ticks=word_lengths)

    # 保存图像
    plt.tight_layout()  # 调整子图间距
    plt.savefig('/Users/fafaya/Desktop/bubbles/speech after selection/word_length_distribution_and_frequency.png')
    plt.show()

# 调用函数生成词长分布图和词长统计图
plot_word_length_distribution_and_frequency(wordlength_result.to_dict('records'))
wordlength_result.to_excel('speech after selection/wordlength.xlsx', sheet_name='wordlength', index=True)