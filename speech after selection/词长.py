import nltk
import pandas as pd
import os

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

        word_len_distribution = {}
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
        wordlength_result.to_excel('speech after selection/wordlength.xlsx', sheet_name='wordlength', index=True)