import nltk
import pandas as pd
from nltk.corpus import stopwords
import os

articles_CNN = pd.read_excel('/Users/fafaya/Desktop/Paris Olympics/Paris Olympics/CNN_content.xlsx')

articles_CNN

punctuation = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
en_stopwords = stopwords.words('english')
result = []

pos_dict = {
 '名词': ['NN','NNS','NNP','NNPS'],
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

for i in range(len(articles_CNN)):
    content = articles_CNN.loc[i]['content']
    words = nltk.word_tokenize(content)
    word_pos = nltk.pos_tag(words)#对分词结构进行词性标注

    metrics = {
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
    word_record = {}#词频字典

    for w_p in word_pos:
        w = w_p[0].lower()
        p = w_p[1]

        if w not in punctuation:
            metrics['总词数'] = metrics.get('总词数') + 1

            if w not in en_stopwords:
                word_record[w] = word_record.get(w,0) + 1

            for k,v in pos_dict.items():
                if p in v:
                    p = k

            pos_tags = list(pos_dict.keys())
            if p in pos_tags:
                metrics[p] = metrics.get(p) + 1

            if p in ['名词', '形容词', '动词', '代词', '数词', '副词']:
                metrics['实词'] = metrics.get('实词') + 1
            elif p in ['介词', '连词', '冠词', '叹词']:
                metrics['虚词'] = metrics.get('虚词') + 1

            if p in ['名词', '形容词', '动词', '副词']:
                    metrics['词汇词'] = metrics.get('词汇词') + 1

    metrics['词汇密度'] = metrics['词汇词'] / metrics['总词数']
    word_record_sorted = dict(sorted(word_record.items(), key=lambda x: x[1], reverse=True))  # 将词频字典按照频数从高到低排序
    metrics['（去除停用词）词频'] = word_record_sorted  # 在metrics字典中添加“词频”

    result.append(metrics)  # result记录每一篇作文的结果

result = pd.DataFrame(result)  # 将列表转换为pd.DataFrame格式，便于展示，且可以直接输出至excel表
result  # jupyter中直接展示dataframe数据

result.to_excel('/Users/fafaya/Desktop/Paris Olympics/Paris Olympics/CNN_content_result.xlsx')
