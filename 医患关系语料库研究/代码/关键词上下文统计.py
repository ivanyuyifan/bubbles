import pandas as pd
import jieba
from collections import Counter
import re

# ========== 1. 文件路径 ==========
input_path = '/Users/fafaya/Desktop/bubbles/医患关系语料库研究/retained_Sina_Comments（筛选后的）.xlsx'
stopwords_path = '/Users/fafaya/Desktop/Linguistics/python学习资料/第四课字词层面的标注与统计/四个中文停用词表/hit_stopwords.txt'
output_path = '/Users/fafaya/Desktop/bubbles/医患关系语料库研究/关键词上下文词频统计.xlsx'

# ========== 2. 加载数据与停用词 ==========
df = pd.read_excel(input_path)

with open(stopwords_path, 'r', encoding='utf-8') as f:
    stopwords = set(line.strip() for line in f if line.strip())

# ========== 3. 自定义关键词列表 ==========
target_keywords = ['医生', '护士', '医患关系', '沟通', '信任']

# ========== 4. 分词 + 抽取关键词上下文窗口 ==========
def get_context_window(text, keyword, window=5):
    text = re.sub(r"[^\u4e00-\u9fa5]", " ", str(text))  # 只保留中文
    words = jieba.lcut(text)
    if keyword not in words:
        return []
    
    windows = []
    for i, word in enumerate(words):
        if word == keyword:
            start = max(i - window, 0)
            end = min(i + window + 1, len(words))
            window_words = [w for w in words[start:end] if w != keyword and w not in stopwords and len(w) > 1]
            windows.extend(window_words)
    return windows

# ========== 5. 构建关键词词频统计表 ==========
keyword_contexts = {}

for kw in target_keywords:
    context_words = []
    for content in df['评论内容'].dropna():
        context_words += get_context_window(content, kw, window=5)
    counter = Counter(context_words)
    keyword_contexts[kw] = counter.most_common(50)  # top 50

# ========== 6. 整理为 DataFrame 并保存 ==========
all_data = []

for kw, pairs in keyword_contexts.items():
    for word, count in pairs:
        all_data.append({'关键词': kw, '共现词': word, '频数': count})

result_df = pd.DataFrame(all_data)
result_df.to_excel(output_path, index=False)

print(f"✅ 关键词上下文词频统计完成，结果保存至：{output_path}")
