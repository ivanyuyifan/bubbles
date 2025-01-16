from ltp import LTP
import os
import pandas as pd
import re  # 用于手动分句
import chardet  # 用于检测文件编码

# 初始化 LTP
ltp = LTP()

# 文件路径
corpus_path = "/Users/fafaya/Desktop/英汉语言对比要用的语料库/学术"
output_excel = "/Users/fafaya/Desktop/英汉语言对比要用的语料库/语料分析结果.xlsx"  # 输出 Excel 文件路径

# 手动实现中文分句
def manual_sent_split(text):
    # 使用正则表达式分句（句号、感叹号、问号）
    sentences = re.split(r"(？|。|！)", text)
    # 将标点符号附加到句子末尾，去掉空字符串
    sentences = [sent + punct if punct else sent for sent, punct in zip(sentences[::2], sentences[1::2])]
    return sentences

# 指标计算函数
def calculate_chinese_metrics(text):
    # 手动分句
    sentences = manual_sent_split(text)
    tokens = []
    pos_tags = []
    heads = []
    labels = []

    for sentence in sentences:
        # 使用 pipeline 进行分词、词性标注和依存分析
        output = ltp.pipeline([sentence], tasks=["cws", "pos", "dep"])
        seg = output.cws[0]  # 分词结果
        pos = output.pos[0]  # 词性标注结果
        dep = output.dep[0]  # 依存分析结果

        # 检查 dep 的数据结构
        if isinstance(dep, dict) and "head" in dep and "label" in dep:
            # 提取 head 和 label
            heads.extend(dep["head"])
            labels.extend(dep["label"])
        else:
            raise ValueError("依存分析结果格式不正确，请检查 LTP 版本和任务配置。")

        tokens.extend(seg)
        pos_tags.extend(pos)

    # 初始化计数
    subordinate_clauses = 0
    passive_phrases = 0
    verb_phrases = 0
    adj_count = 0
    noun_count = 0
    prep_count = 0

    # 遍历依存关系和词性标注
    for i, (token, pos_tag, head, label) in enumerate(zip(tokens, pos_tags, heads, labels)):
        print(f"Token: {token}, POS: {pos_tag}, Head: {head}, Label: {label}")
        
        # 从属句识别
        subordinate_conjunctions = ["因为", "虽然", "如果", "但是", "由于", "尽管", "即使", "假如"]
        if label in ["ADV", "VOB", "ATT", "SBV"] and token in subordinate_conjunctions:
            print(f"Found subordinate clause: {token}")
            subordinate_clauses += 1
        
        # 被动语态识别
        passive_markers = ["被", "让", "给"]
        if pos_tag == "p" and token in passive_markers and label in ["SBV", "VOB"]:
            print(f"Found passive phrase: {token}")
            passive_phrases += 1
        
        # 动词短语复杂度
        if pos_tag == "v":
            verb_phrases += 1
        
        # 名词修饰统计
        if pos_tag == "a":  # 形容词
            adj_count += 1
        if pos_tag == "n":  # 名词
            noun_count += 1
        if pos_tag == "p":  # 介词
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
    if filename.endswith(".ZH.txt"):
        file_path = os.path.join(corpus_path, filename)
        
        # 检测文件编码
        with open(file_path, "rb") as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            encoding = result["encoding"]
        
        # 使用检测到的编码读取文件
        try:
            with open(file_path, "r", encoding=encoding) as zh_file:
                zh_text = zh_file.read()
        except UnicodeDecodeError:
            # 如果检测到的编码失败，尝试其他编码
            try:
                with open(file_path, "r", encoding="utf-8") as zh_file:
                    zh_text = zh_file.read()
            except UnicodeDecodeError:
                with open(file_path, "r", encoding="gbk") as zh_file:
                    zh_text = zh_file.read()
        
        # 计算中文指标
        zh_metrics = calculate_chinese_metrics(zh_text)
        # 添加文件名和指标到结果
        results.append({
            "File": filename,
            "MLS": zh_metrics["MLS"],
            "C/S": zh_metrics["C/S"],
            "PVR": zh_metrics["PVR"],
            "VP/C": zh_metrics["VP/C"],
            "Adj/N": zh_metrics["Adj/N"],
            "Prep/N": zh_metrics["Prep/N"]
        })

# 将结果保存到 Excel 表格
df = pd.DataFrame(results)  # 将结果转换为 DataFrame
df.to_excel(output_excel, index=False, sheet_name="Analysis Results")  # 保存为 Excel 文件

print(f"分析结果已保存到 {output_excel}")