import jieba.analyse
import pandas as pd

# 文件路径与标签
files = {
    "/Users/fafaya/Desktop/宫老师的两封情书.txt": "情书",
    "/Users/fafaya/Desktop/宫老师的后期小作文.txt": "后期小作文"
}

# 存储关键词结果
tfidf_keywords = []
textrank_keywords = []

for path, label in files.items():
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()

    # TF-IDF 提取
    tfidf = jieba.analyse.extract_tags(text, topK=30, withWeight=True)
    for word, weight in tfidf:
        tfidf_keywords.append({
            "来源": label,
            "方法": "TF-IDF",
            "关键词": word,
            "权重": round(weight, 4)
        })

    # TextRank 提取
    textrank = jieba.analyse.textrank(text, topK=30, withWeight=True)
    for word, weight in textrank:
        textrank_keywords.append({
            "来源": label,
            "方法": "TextRank",
            "关键词": word,
            "权重": round(weight, 4)
        })

# 合并保存
all_keywords = pd.DataFrame(tfidf_keywords + textrank_keywords)
all_keywords.to_csv("/Users/fafaya/Desktop/关键词提取_TFIDF_TextRank.csv", index=False, encoding='utf-8-sig')
print("✅ 关键词提取完成，已保存至：关键词提取_TFIDF_TextRank.csv")
