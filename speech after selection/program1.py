import nltk
import pandas as pd
from nltk.corpus import stopwords
from openpyxl.workbook import Workbook
import os

punctuation =  r"""!"#$%&'’()*+,-./:;<=>?@[\]^_`{|}~"""
en_stopwords = stopwords.words('english')
result = []#用来记录演讲稿的分析结果

pos_dict = {'名词': ['NN','NNS','NNP','NNPS'],
 '形容词': ['JJ','JJR','JJS'],
 '动词': ['VB','VBD','VBG','VBN','VBP','VBZ','MD'],
 '代词': ['PRP','WP','WP$'],
 '数词': ['CD'],
 '副词': ['RB','RBR','RBS','WRB'],
 '介词': ['IN'],
 '连词': ['CC','IN'],
 '冠词': ['DT'],
 '叹词': ['UH'],
 }

#定义打开文件的函数（虽然感觉没啥用）
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

        #最终输出的结果就是metrics
        metrics = { '文件名': filename,
        '总词数': 0,
        '名词': 0,
        '形容词': 0,
        '动词': 0,
        '代词': 0,
        '数词': 0,
        '副词': 0,
        '介词': 0,
        '连词': 0,
        '冠词': 0,
        '叹词': 0,
        '实词': 0,
        '虚词': 0,
        '词汇词': 0
        }
        word_frequency = {}#词频字典

        for w_p in word_pos:
            w = w_p[0].lower()
            p = w_p[1]

            if w not in punctuation:
                metrics['总词数'] = metrics.get('总词数') + 1

                if w not in en_stopwords:
                    word_frequency[w] = word_frequency.get(w, 0) + 1

                for k, v in pos_dict.items():
                    if p in v:
                        p = k

                pos_tags = list(pos_dict.keys())
                if p in pos_tags:
                    metrics[p] = metrics.get(p) + 1

                if p in ['名词','形容词','动词','代词','数词','副词']:
                    metrics['实词'] = metrics.get('实词') + 1
                elif p in ['介词','连词','冠词','叹词']:
                    metrics['虚词'] = metrics.get('虚词') + 1

                if p in ['名词','形容词','动词','副词']:
                    metrics['词汇词'] = metrics.get('词汇词') + 1


        metrics['词汇密度'] = metrics['词汇词'] / metrics['总词数']
        word_frequency_sorted = dict(sorted(word_frequency.items(), key=lambda x:x[1], reverse = True))
        metrics['（去除停用词）词频'] = word_frequency_sorted

        result.append(metrics)

result = pd.DataFrame(result)

result.to_excel('Word_index.xlsx',sheet_name='Word_index',index=True)

