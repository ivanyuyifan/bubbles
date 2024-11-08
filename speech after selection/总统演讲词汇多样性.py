import math
import os
import nltk
import pandas as pd

result_duoyangxing = []

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
        word_pos = nltk.pos_tag(words)
#记录多样性的字典
        metrics = {'不重复的单词数': 0,
 'TTR（type/token）': 0,
 'RTTR': 0,
 'CTTR': 0,
 'LogTTR': 0,
 'Uber': 0,
 }
        token_num = 0
        words_dedup = []#记录不重复的单词数量

        for w in words:
            w = w.lower()
            if w != 'SYM':
                token_num =token_num + 1

                if w not in words_dedup:
                    words_dedup.append(w)

        type_num = len(words_dedup)#type
        TTR = type_num / token_num
        RTTR = type_num / math.sqrt(token_num)
        CTTR = type_num / math.sqrt(2 * token_num)
        LogTTR = math.log10(type_num)
        Uber = math.log10(token_num) * math.log10(token_num) / math.log10(token_num/type_num)
        metrics = {'不重复的单词数': type_num,
 'TTR（type/token）':TTR,
 'RTTR': RTTR,
 'CTTR': CTTR,
 'LogTTR': LogTTR,
 'Uber': Uber,
 }
        result_duoyangxing.append(metrics)

result_duoyangxing = pd.DataFrame(result_duoyangxing)
result_duoyangxing.to_excel('duoyangxing.xlsx', sheet_name='duoyangxing', index=True)
