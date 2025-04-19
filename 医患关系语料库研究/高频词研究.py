import pandas as pd
import jieba
from collections import Counter
import re

# 文件路径
input_path = '/Users/fafaya/Desktop/bubbles/医患关系语料库研究/retained_Sina_Comments（筛选后的）.xlsx'
output_path = '/Users/fafaya/Desktop/bubbles/医患关系语料库研究/word_frequency_top100.xlsx'

# 加载语料
df = pd.read_excel(input_path)

# 停用词表（你也可以用外部文本文件）
stopwords_path = '/Users/fafaya/Desktop/Linguistics/python学习资料/第四课字词层面的标注与统计/四个中文停用词表/hit_stopwords.txt'

# 读取停用词文件（假设一行一个词）
with open(stopwords_path, 'r', encoding='utf-8') as f:
    stopwords = set(line.strip() for line in f if line.strip())
    
# 文本清洗 + 分词
def clean_and_tokenize(text):
    text = str(text)
    text = re.sub(r"[^\u4e00-\u9fa5]", " ", text)  # 仅保留中文
    words = jieba.lcut(text)
    return [w for w in words if w not in stopwords and len(w) > 1]

# 分词并合并
all_words = []
for content in df['评论内容'].dropna():
    all_words.extend(clean_and_tokenize(content))

# 统计词频
word_counts = Counter(all_words)
top_words = word_counts.most_common(100)

# 保存为 Excel
top_df = pd.DataFrame(top_words, columns=['词语', '频数'])
top_df.to_excel(output_path, index=False)

print(f"✅ Top 100 高频词统计完成，保存至：{output_path}")
