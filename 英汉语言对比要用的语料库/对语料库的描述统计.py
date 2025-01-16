import os
import pandas as pd
import chardet
import jieba
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk
import re
import math

# 下载 nltk 数据
nltk.download("punkt")

# 文件路径
corpus_path = "/Users/fafaya/Desktop/英汉语言对比要用的语料库/学术"

# 初始化统计信息
data = {
    "Language": ["English", "Chinese"],
    "Number": [0, 0],  # 文件数量
    "Words": [0, 0],  # 总词数
    "Maximum": [0, 0],  # 最大句子长度
    "Minimum": [float("inf"), float("inf")],  # 最小句子长度
    "Mean": [0, 0],  # 平均句子长度
    "SD": [0, 0]  # 句子长度的标准差
}

# 中文分句函数
def chinese_sent_tokenize(text):
    # 使用正则表达式按标点符号分句
    sentences = re.split(r"(？|。|！)", text)
    # 将标点符号附加到句子末尾
    sentences = [sent + punct if punct else sent for sent, punct in zip(sentences[::2], sentences[1::2])]
    return [sent.strip() for sent in sentences if sent.strip()]

# 遍历文件
for filename in sorted(os.listdir(corpus_path)):
    if filename.endswith(".txt"):
        file_path = os.path.join(corpus_path, filename)
        
        # 检测文件编码
        with open(file_path, "rb") as file:
            raw_data = file.read()
            result = chardet.detect(raw_data)
            encoding = result["encoding"]
        
        # 使用检测到的编码读取文件
        try:
            with open(file_path, "r", encoding=encoding) as file:
                text = file.read()
                
                # 判断语言
                if filename.endswith(".EN.txt"):
                    idx = 0  # 英文
                    # 使用 nltk 分句和分词
                    sentences = sent_tokenize(text)
                    word_counts = [len(word_tokenize(sentence)) for sentence in sentences if sentence.strip()]
                else:
                    idx = 1  # 中文
                    # 使用自定义分句函数和 jieba 分词
                    sentences = chinese_sent_tokenize(text)
                    word_counts = [len(list(jieba.cut(sentence))) for sentence in sentences if sentence.strip()]
                
                # 更新统计信息
                data["Number"][idx] += 1
                data["Words"][idx] += sum(word_counts)
                data["Maximum"][idx] = max(data["Maximum"][idx], max(word_counts)) if word_counts else data["Maximum"][idx]
                data["Minimum"][idx] = min(data["Minimum"][idx], min(word_counts)) if word_counts else data["Minimum"][idx]
                
                # 计算均值和标准差
                if word_counts:
                    mean = sum(word_counts) / len(word_counts)
                    variance = sum((x - mean) ** 2 for x in word_counts) / len(word_counts)
                    std_dev = math.sqrt(variance)
                    
                    # 更新均值和标准差
                    data["Mean"][idx] += mean
                    data["SD"][idx] += std_dev
        except UnicodeDecodeError:
            # 如果检测到的编码失败，尝试其他常见编码
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    text = file.read()
                    
                    if filename.endswith(".EN.txt"):
                        idx = 0
                        sentences = sent_tokenize(text)
                        word_counts = [len(word_tokenize(sentence)) for sentence in sentences if sentence.strip()]
                    else:
                        idx = 1
                        sentences = chinese_sent_tokenize(text)
                        word_counts = [len(list(jieba.cut(sentence))) for sentence in sentences if sentence.strip()]
                    
                    data["Number"][idx] += 1
                    data["Words"][idx] += sum(word_counts)
                    data["Maximum"][idx] = max(data["Maximum"][idx], max(word_counts)) if word_counts else data["Maximum"][idx]
                    data["Minimum"][idx] = min(data["Minimum"][idx], min(word_counts)) if word_counts else data["Minimum"][idx]
                    
                    if word_counts:
                        mean = sum(word_counts) / len(word_counts)
                        variance = sum((x - mean) ** 2 for x in word_counts) / len(word_counts)
                        std_dev = math.sqrt(variance)
                        
                        data["Mean"][idx] += mean
                        data["SD"][idx] += std_dev
            except UnicodeDecodeError:
                with open(file_path, "r", encoding="gbk") as file:
                    text = file.read()
                    
                    if filename.endswith(".EN.txt"):
                        idx = 0
                        sentences = sent_tokenize(text)
                        word_counts = [len(word_tokenize(sentence)) for sentence in sentences if sentence.strip()]
                    else:
                        idx = 1
                        sentences = chinese_sent_tokenize(text)
                        word_counts = [len(list(jieba.cut(sentence))) for sentence in sentences if sentence.strip()]
                    
                    data["Number"][idx] += 1
                    data["Words"][idx] += sum(word_counts)
                    data["Maximum"][idx] = max(data["Maximum"][idx], max(word_counts)) if word_counts else data["Maximum"][idx]
                    data["Minimum"][idx] = min(data["Minimum"][idx], min(word_counts)) if word_counts else data["Minimum"][idx]
                    
                    if word_counts:
                        mean = sum(word_counts) / len(word_counts)
                        variance = sum((x - mean) ** 2 for x in word_counts) / len(word_counts)
                        std_dev = math.sqrt(variance)
                        
                        data["Mean"][idx] += mean
                        data["SD"][idx] += std_dev

# 计算均值和标准差的平均值
data["Mean"][0] = data["Mean"][0] / data["Number"][0] if data["Number"][0] else 0
data["Mean"][1] = data["Mean"][1] / data["Number"][1] if data["Number"][1] else 0

data["SD"][0] = data["SD"][0] / data["Number"][0] if data["Number"][0] else 0
data["SD"][1] = data["SD"][1] / data["Number"][1] if data["Number"][1] else 0

# 创建 DataFrame
df = pd.DataFrame(data)

# 输出表格
print(df)

# 保存为 Excel 文件
df.to_excel("corpus_summary_statistics.xlsx", index=False)