import os
import pandas as pd
import spacy  # 用于英文的句法分析
import re  # 用于手动分句
import chardet  # 用于检测文件编码

# 加载 spaCy 的英文模型
nlp = spacy.load("en_core_web_sm")

# 文件路径
corpus_path = "/Users/fafaya/Desktop/英汉语言对比要用的语料库/学术"
output_excel = "/Users/fafaya/Desktop/英汉语言对比要用的语料库/英文语料分析结果.xlsx"  # 输出 Excel 文件路径

# 手动实现英文分句
def manual_sent_split(text):
    # 使用正则表达式分句（句号、感叹号、问号）
    sentences = re.split(r"(?<=[.!?])\s+", text)
    return sentences

# 指标计算函数
def calculate_english_metrics(text):
    # 手动分句
    sentences = manual_sent_split(text)
    tokens = []
    pos_tags = []
    heads = []
    labels = []

    for sentence in sentences:
        # 使用 spaCy 进行句法分析
        doc = nlp(sentence)
        for token in doc:
            tokens.append(token.text)
            pos_tags.append(token.pos_)
            heads.append(token.head.i)
            labels.append(token.dep_)

    # 初始化计数
    subordinate_clauses = 0
    passive_phrases = 0
    verb_phrases = 0
    adj_count = 0
    noun_count = 0
    prep_count = 0

    # 遍历依存关系和词性标注
    for i, (token, pos_tag, head, label) in enumerate(zip(tokens, pos_tags, heads, labels)):
        # 从属句识别
        if label in ["mark", "advcl", "acl", "ccomp"]:
            subordinate_clauses += 1
        
        # 被动语态识别
        if pos_tag == "AUX" and token.lower() in ["be", "been", "was", "were"]:
            # 重新获取当前 token 的 spaCy 对象
            doc = nlp(sentence)  # 重新分析句子
            if i < len(doc):  # 确保索引不超出范围
                for child in doc[i].children:
                    if child.dep_ == "auxpass":
                        passive_phrases += 1
                        break
        
        # 动词短语复杂度
        if pos_tag == "VERB":
            verb_phrases += 1
        
        # 名词修饰统计
        if pos_tag == "ADJ":  # 形容词
            adj_count += 1
        if pos_tag == "NOUN":  # 名词
            noun_count += 1
        if pos_tag == "ADP":  # 介词
            prep_count += 1

    # 指标计算
    num_sentences = len(sentences)
    mls = len(tokens) / num_sentences if num_sentences else 0
    c_s = subordinate_clauses / num_sentences if num_sentences else 0
    vp_c = verb_phrases / num_sentences if num_sentences else 0
    adj_n = adj_count / noun_count if noun_count else 0
    prep_n = prep_count / noun_count if noun_count else 0

    return {
        "MLS": mls,
        "C/S": c_s,
        "PVR": passive_phrases / len(tokens) if tokens else 0,
        "VP/C": vp_c,
        "Adj/N": adj_n,
        "Prep/N": prep_n
    }

# 遍历语料库文件夹
results = []
for filename in sorted(os.listdir(corpus_path)):
    if filename.endswith(".EN.txt"):  # 只处理英文文件
        file_path = os.path.join(corpus_path, filename)
        
        # 检测文件编码
        with open(file_path, "rb") as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            encoding = result["encoding"]
        
        # 使用检测到的编码读取文件
        try:
            with open(file_path, "r", encoding=encoding) as en_file:
                en_text = en_file.read()
        except UnicodeDecodeError:
            # 如果检测到的编码失败，尝试其他编码
            try:
                with open(file_path, "r", encoding="utf-8") as en_file:
                    en_text = en_file.read()
            except UnicodeDecodeError:
                with open(file_path, "r", encoding="gbk") as en_file:
                    en_text = en_file.read()
        
        # 计算英文指标
        en_metrics = calculate_english_metrics(en_text)
        # 添加文件名和指标到结果
        results.append({
            "File": filename,
            "MLS": en_metrics["MLS"],
            "C/S": en_metrics["C/S"],
            "PVR": en_metrics["PVR"],
            "VP/C": en_metrics["VP/C"],
            "Adj/N": en_metrics["Adj/N"],
            "Prep/N": en_metrics["Prep/N"]
        })

# 将结果保存到 Excel 表格
df = pd.DataFrame(results)  # 将结果转换为 DataFrame
df.to_excel(output_excel, index=False, sheet_name="Analysis Results")  # 保存为 Excel 文件

print(f"英文语料分析结果已保存到 {output_excel}")