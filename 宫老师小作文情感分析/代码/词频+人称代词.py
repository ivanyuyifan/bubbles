import jieba
from collections import Counter
import pandas as pd

# 自定义代词表（可扩充）
pronouns = ["我", "你", "他", "她", "我们", "你们", "他们", "自己", "咱们"]

# 文件路径
files = {
    "/Users/fafaya/Desktop/宫老师的两封情书.txt": "情书",
    "/Users/fafaya/Desktop/宫老师的后期小作文.txt": "后期小作文"
}

# 存储所有结果
all_words = []
pronoun_counts = []

for path, label in files.items():
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    words = jieba.lcut(text)
    word_freq = Counter(words)

    # 保存总词频（可供词云使用）
    for word, count in word_freq.items():
        if len(word.strip()) > 1:  # 去除单字词（如“了”“的”）
            all_words.append({
                "来源": label,
                "词语": word,
                "频次": count
            })

    # 统计代词频率
    for p in pronouns:
        pronoun_counts.append({
            "来源": label,
            "代词": p,
            "频次": word_freq[p]
        })

# 输出为CSV
pd.DataFrame(all_words).to_csv("/Users/fafaya/Desktop/word_freq.csv", index=False, encoding="utf-8-sig")
pd.DataFrame(pronoun_counts).to_csv("/Users/fafaya/Desktop/pronoun_freq.csv", index=False, encoding="utf-8-sig")

print("✅ 已导出：词频统计 (word_freq.csv)，代词统计 (pronoun_freq.csv)")
