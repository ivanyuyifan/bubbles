#分析目的：1.分析“水灵灵地”喜欢和什么词一起搭配使用 
# 2.情感分析看“水灵灵地xx”偏什么情绪 
# 3.提取主题，LDA建模，看网友喜欢用“水灵灵地”形容什么
import jieba
import jieba.posseg as pseg
import nltk
from collections import Counter
from math import log, sqrt
import pandas as pd

# 确保安装 nltk 的 bigram 和 trigram 模块
nltk.download('punkt')

# 添加自定义词汇，设置词频为 5000，词性为 'ad'
jieba.add_word("水灵灵地", freq=5000, tag="ad")

# 定义函数：统计“水灵灵地”后紧邻的词语频次
def analyze_following_words(corpus, target_word):
    # 分词
    word_list = list(jieba.cut(corpus))

    # 遍历分词结果，找到目标词后面的词
    following_words = []
    for i in range(len(word_list) - 1):  # 遍历到倒数第二个词
        if word_list[i] == target_word:
            following_words.append(word_list[i + 1])  # 记录目标词后的词

    # 统计频次
    word_freq = Counter(following_words)
    return word_freq

def extract_ngrams_with_association(corpus, target_word):
    # 分词
    word_list = list(jieba.cut(corpus))

    # 生成 bigram 和 trigram
    bigrams = list(nltk.bigrams(word_list))
    trigrams = list(nltk.trigrams(word_list))

    # 统计词频
    word_freq = Counter(word_list)  # 单词频率
    bigram_freq = Counter(bigrams)  # 双词频率
    trigram_freq = Counter(trigrams)  # 三词频率

    # 计算搭配强度 (PMI 和 t-score) for bigram
    bigram_scores = {}
    total_words = len(word_list)
    for bigram in bigram_freq:
        w1, w2 = bigram
        p_w1_w2 = bigram_freq[bigram] / total_words  # 联合概率
        p_w1 = word_freq[w1] / total_words  # w1 的概率
        p_w2 = word_freq[w2] / total_words  # w2 的概率

        #以下为计算搭配强度的指标
        pmi = log(p_w1_w2 / (p_w1 * p_w2), 2) if p_w1_w2 > 0 else 0
        t_score = (bigram_freq[bigram] - total_words * p_w1 * p_w2) / sqrt(bigram_freq[bigram])

        bigram_scores[bigram] = {
            "PMI": pmi,
            "t-score": t_score,
            "Frequency": bigram_freq[bigram]  # 添加频次到结果中
        }

    # 筛选包含目标词的 bigram
    target_bigrams = {k: v for k, v in bigram_scores.items() if target_word in k}

    return bigrams, trigrams, target_bigrams

# 主函数
def main():
    # 读取语料
    filepath = '/Users/fafaya/Desktop/bubbles/水灵灵地/output.txt'
    with open(filepath, 'r', encoding='utf-8') as f:
        corpus_content = f.read()

    target_word = "水灵灵地"

    # 统计“水灵灵地”后面紧邻的词语频次
    following_word_freq = analyze_following_words(corpus_content, target_word)
    following_word_data = [{"Word": word, "Frequency": freq} for word, freq in following_word_freq.items()]

    # 生成 bigram、trigram 并计算搭配强度
    _, _, target_bigrams = extract_ngrams_with_association(corpus_content, target_word)

    # 将 target_bigrams 转换为列表
    bigram_data = [{"Bigram": f"{k[0]} {k[1]}", "PMI": v["PMI"], "T-score": v["t-score"], "Frequency": v["Frequency"]} for k, v in target_bigrams.items()]

    # 将结果保存到 Excel 文件
    output_path = "/Users/fafaya/Desktop/bubbles/水灵灵地/水灵灵地词频与搭配_results.xlsx"
    with pd.ExcelWriter(output_path) as writer:
        # 保存“后接词频统计”到 Sheet
        pd.DataFrame(following_word_data).sort_values(by="Frequency", ascending=False).to_excel(writer, sheet_name="Following Words", index=False)

        # 保存“搭配强度 (bigram)”到 Sheet
        pd.DataFrame(bigram_data).sort_values(by="PMI", ascending=True).to_excel(writer, sheet_name="Bigram Association", index=False)

    print(f"结果已保存到: {'水灵灵地词频与搭配'}")

# 运行主函数
if __name__ == "__main__":
    main()

