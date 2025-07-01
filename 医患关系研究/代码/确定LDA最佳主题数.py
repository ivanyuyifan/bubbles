import pandas as pd
import os
import jieba
from gensim import corpora, models
from gensim.models.coherencemodel import CoherenceModel
import matplotlib.pyplot as plt
import pyLDAvis
import pyLDAvis.gensim_models as gensimvis
from tqdm import tqdm

# --- 1. 配置区 ---
# 您只需要修改这个区域的参数

# 输入的、已经预处理好的CSV文件路径
INPUT_CSV_PATH = '/Users/fafaya/Desktop/医患关系研究/预处理后语料/weibo_data_cleaned_master.csv'

# 停用词文件路径
STOPWORDS_PATH = '/Users/fafaya/Desktop/医患关系研究/hit_stopwords.txt'

# 所有结果的输出目录
OUTPUT_DIR = 'lda_results'

# 寻找最佳主题数时，要测试的范围
# 例如，range(2, 16) 表示测试主题数为 2, 3, 4, ..., 15
TOPIC_RANGE = range(2, 16) 

# 最终模型每个主题要展示的关键词数量
NUM_TOP_WORDS = 15

# --- 主程序 ---

def lda_modeling_pipeline():
    """一个完整的LDA建模与分析流程"""
    
    # --- 2. 加载和准备数据 ---
    print("--- 步骤1: 加载预处理后的数据 ---")
    try:
        df = pd.read_csv(INPUT_CSV_PATH)
        df.dropna(subset=['微博内容_清洗后'], inplace=True)
        print(f"成功加载数据，共 {len(df)} 条微博用于建模。\n")
    except FileNotFoundError:
        print(f"错误: 文件未找到，请检查路径 -> {INPUT_CSV_PATH}")
        return

    # --- 3. 文本分词与过滤 ---
    print("--- 步骤2: 对微博内容进行分词与停用词过滤 ---")
    try:
        with open(STOPWORDS_PATH, 'r', encoding='utf-8') as f:
            stopwords = {line.strip() for line in f}
    except FileNotFoundError:
        print(f"警告: 停用词文件未找到 ({STOPWORDS_PATH})，将不使用停用词过滤。")
        stopwords = set()

    texts = []
    for text in tqdm(df['微博内容_清洗后'], desc="分词与过滤中"):
        words = [w for w in jieba.lcut(str(text)) if w.strip() and w not in stopwords and len(w) > 1]
        texts.append(words)
    print("文本预处理完成。\n")

    # --- 4. 构建Gensim词典和语料库 ---
    print("--- 步骤3: 构建词典和词袋(BoW)语料库 ---")
    dictionary = corpora.Dictionary(texts)
    # 过滤掉出现次数少于5次，或者在超过50%的文档中都出现的词
    dictionary.filter_extremes(no_below=5, no_above=0.5)
    corpus = [dictionary.doc2bow(text) for text in texts]
    print("词典和语料库构建完毕。\n")

    # --- 5. 寻找最佳主题数量 (K值) ---
    print("--- 步骤4: 计算不同主题数下的一致性得分，以寻找最佳K值 ---")
    coherence_scores = []
    for num_topics in tqdm(list(TOPIC_RANGE), desc="寻找最佳主题数"):
        lda_model = models.LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics, passes=10, random_state=100)
        coherence_model_lda = CoherenceModel(model=lda_model, texts=texts, dictionary=dictionary, coherence='c_v')
        coherence_scores.append(coherence_model_lda.get_coherence())
    
    # 绘制一致性得分曲线
    plt.figure(figsize=(12, 7))
    plt.plot(TOPIC_RANGE, coherence_scores)
    plt.xlabel("Number of Topics(K)")
    plt.ylabel("Coherence Score")
    plt.title("Theme-Consistency Score Curve")
    plt.grid(True)
    
    # 确保输出目录存在
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    coherence_plot_path = os.path.join(OUTPUT_DIR, 'coherence_curve.png')
    plt.savefig(coherence_plot_path)
    print(f"\n一致性曲线已保存至: {coherence_plot_path}")
    print("请查看该图片，选择一致性得分最高（或开始下降的拐点处）的主题数作为最佳K值。\n")
    # plt.show() # 如果在Jupyter环境中，可以取消注释以直接显示

    # --- 6. 根据选择的K值，训练最终模型 ---
    try:
        optimal_k = int(input("请输入您根据曲线选择的最佳主题数 (K值): "))
    except ValueError:
        print("输入无效，将使用默认值 K=8。")
        optimal_k = 8
        
    print(f"\n--- 步骤5: 使用 K={optimal_k} 训练最终的LDA模型 ---")
    final_lda_model = models.LdaModel(corpus=corpus, id2word=dictionary, num_topics=optimal_k, passes=20, random_state=100)
    print("最终模型训练完毕！\n")

    # --- 7. 输出与保存结果 ---
    print(f"--- 步骤6: 输出主题关键词并生成离线可视化报告 ---")
    
    # a. 在控制台打印每个主题的关键词
    print(f"每个主题的 Top {NUM_TOP_WORDS} 关键词:")
    topics = final_lda_model.print_topics(num_words=NUM_TOP_WORDS)
    for topic in topics:
        print(topic)
        
    # b. 生成pyLDAvis离线HTML文件
    print("\n正在生成pyLDAvis可视化报告...")
    vis_data = gensimvis.prepare(final_lda_model, corpus, dictionary, sort_topics=False)
    vis_html_path = os.path.join(OUTPUT_DIR, 'lda_visualization.html')
    pyLDAvis.save_html(vis_data, vis_html_path)
    print(f"可视化报告已成功生成！这是一个独立的HTML文件，您可以用浏览器离线打开。")
    print(f"文件路径: {vis_html_path}\n")

    # c. 保存模型、词典和语料库，方便以后直接加载使用
    final_lda_model.save(os.path.join(OUTPUT_DIR, 'lda_model.model'))
    dictionary.save(os.path.join(OUTPUT_DIR, 'dictionary.gensim'))
    corpora.MmCorpus.serialize(os.path.join(OUTPUT_DIR, 'corpus.mm'), corpus)
    print("模型、词典和语料库已保存，方便未来直接加载分析。\n")
    
    print("="*80)
    print("LDA建模流程全部完成！")
    print("="*80)

if __name__ == '__main__':
    lda_modeling_pipeline()