import os
import pandas as pd
import re
from snownlp import SnowNLP

def split_sentences(text):
    # 简单的中文分句（也可使用NLP工具分句更准确）
    sentences = re.split(r'(。|！|\!|？|\?)', text)
    full_sentences = []
    for i in range(0, len(sentences) - 1, 2):
        full_sentences.append(sentences[i] + sentences[i+1])
    return [s.strip() for s in full_sentences if s.strip()]

def analyze_file(file_path, file_label):
    with open(file_path, 'r', encoding='utf-8') as f:
        raw_text = f.read()
    sentences = split_sentences(raw_text)
    results = []
    for i, sentence in enumerate(sentences):
        s = SnowNLP(sentence)
        results.append({
            "来源": file_label,
            "句号": i + 1,
            "句子": sentence,
            "情感得分": round(s.sentiments, 4)
        })
    return results

# 设置文件路径
files = {
    "/Users/fafaya/Desktop/宫老师的两封情书.txt": "情书",
    "/Users/fafaya/Desktop/宫老师的后期小作文.txt": "后期小作文"
}

# 分析所有文件
all_results = []
for path, label in files.items():
    all_results.extend(analyze_file(path, label))

# 保存为 CSV
df = pd.DataFrame(all_results)
output_path = "/Users/fafaya/Desktop/宫老师_情感分析_by_sentence.csv"
df.to_csv(output_path, index=False, encoding='utf-8-sig')

print(f"情感分析完成，已保存至：{output_path}")
