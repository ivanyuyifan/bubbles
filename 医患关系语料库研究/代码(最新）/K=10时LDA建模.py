import pandas as pd
import os
import jieba
import pyLDAvis
import pyLDAvis.gensim_models as gensimvis
from gensim import corpora, models
from tqdm import tqdm

# ==============================================================================
# 1. 参数配置区
# ==============================================================================
# 输入的、已经预处理好的CSV文件路径
INPUT_CSV_PATH = '/Users/fafaya/Desktop/医患关系研究/预处理后语料/weibo_data_cleaned_master.csv'

# 停用词文件路径
STOPWORDS_PATH = '/Users/fafaya/Desktop/医患关系研究/hit_stopwords.txt'

# 所有结果的输出目录
OUTPUT_DIR = 'final_lda_results'

# 您已确定的最佳主题数
OPTIMAL_K = 10

# 每个主题要展示和保存的关键词数量
NUM_TOP_WORDS = 20

# Gensim LDA模型参数
# passes: 模型训练的迭代次数，次数越多模型可能越稳定，但耗时越长
LDA_PASSES = 30 
# random_state: 随机种子，确保每次运行结果可复现
RANDOM_STATE = 100

# ==============================================================================
# 2. 功能函数区
# ==============================================================================

def load_and_prepare_data(csv_path, stopwords_path):
    """加载数据，并进行分词、停用词过滤等文本准备工作。"""
    print("--- 步骤1: 加载并准备文本数据 ---")
    try:
        df = pd.read_csv(csv_path)
        df.dropna(subset=['微博内容_清洗后'], inplace=True)
        print(f"成功加载数据，共 {len(df)} 条微博用于建模。")
    except FileNotFoundError:
        print(f"错误: 文件未找到，请检查路径 -> {csv_path}")
        return None, None

    try:
        with open(stopwords_path, 'r', encoding='utf-8') as f:
            stopwords = {line.strip() for line in f}
    except FileNotFoundError:
        print(f"警告: 停用词文件未找到 ({stopwords_path})，将不使用停用词过滤。")
        stopwords = set()

    texts = []
    for text in tqdm(df['微博内容_清洗后'], desc="分词与过滤中"):
        words = [w for w in jieba.lcut(str(text)) if w.strip() and w not in stopwords and len(w) > 1]
        texts.append(words)
    
    print("文本数据准备完毕。\n")
    return texts, df # 同时返回原始DataFrame，方便后续合并

def train_lda_model(texts, num_topics):
    """构建词典、语料库，并训练最终的LDA模型。"""
    print(f"--- 步骤2: 使用 K={num_topics} 训练最终LDA模型 ---")
    
    # 构建词典
    dictionary = corpora.Dictionary(texts)
    dictionary.filter_extremes(no_below=5, no_above=0.5)
    
    # 构建词袋(BoW)语料库
    corpus = [dictionary.doc2bow(text) for text in texts]
    
    # 训练LDA模型
    lda_model = models.LdaModel(
        corpus=corpus, 
        id2word=dictionary, 
        num_topics=num_topics, 
        passes=LDA_PASSES, 
        random_state=RANDOM_STATE
    )
    print("最终模型训练完毕！\n")
    return lda_model, dictionary, corpus

def generate_lda_outputs(lda_model, corpus, dictionary, df_original):
    """生成并保存所有分析结果，包括关键词、可视化报告和文档-主题分布。"""
    print("--- 步骤3: 生成并保存分析结果 ---")
    
    # 确保输出目录存在
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # a. 保存每个主题的关键词到txt文件
    topics_path = os.path.join(OUTPUT_DIR, 'topics_keywords.txt')
    with open(topics_path, 'w', encoding='utf-8') as f:
        f.write(f"LDA Model Topics (K={lda_model.num_topics})\n")
        f.write("="*30 + "\n")
        topics = lda_model.print_topics(num_words=NUM_TOP_WORDS)
        for topic in topics:
            f.write(str(topic) + "\n")
    print(f"  -> 主题关键词列表已保存至: {topics_path}")

    # b. 生成pyLDAvis离线HTML文件
    print("  -> 正在生成pyLDAvis可视化报告 (此步骤可能需要一些时间)...")
    vis_data = gensimvis.prepare(lda_model, corpus, dictionary, sort_topics=False)
    vis_html_path = os.path.join(OUTPUT_DIR, 'lda_visualization.html')
    pyLDAvis.save_html(vis_data, vis_html_path)
    print(f"  -> 可视化报告已成功生成！文件路径: {vis_html_path}")

    # c. 计算并保存每篇微博的主题分布到CSV文件
    print("  -> 正在计算每篇微博的主题分布...")
    topic_distributions = []
    for doc_bow in tqdm(corpus, desc="计算主题分布中"):
        doc_topics = lda_model.get_document_topics(doc_bow, minimum_probability=0)
        topic_prob_list = [prob for _, prob in sorted(doc_topics, key=lambda x: x[0])]
        topic_distributions.append(topic_prob_list)
    
    topic_names = [f"Topic_{i}" for i in range(lda_model.num_topics)]
    doc_topic_df = pd.DataFrame(topic_distributions, columns=topic_names)
    
    # 将主题分布与原始数据（部分列）合并
    final_df = pd.concat([df_original.reset_index(drop=True), doc_topic_df], axis=1)
    
    doc_topics_path = os.path.join(OUTPUT_DIR, 'document_topic_distribution.csv')
    final_df.to_csv(doc_topics_path, index=False, encoding='utf-8-sig')
    print(f"  -> 每篇微博的主题分布已保存至: {doc_topics_path}\n")

# ==============================================================================
# 3. 主程序入口
# ==============================================================================
if __name__ == '__main__':
    # 运行完整的建模与分析流程
    texts, original_df = load_and_prepare_data(INPUT_CSV_PATH, STOPWORDS_PATH)
    
    if texts and original_df is not None:
        lda_model, dictionary, corpus = train_lda_model(texts, OPTIMAL_K)
        generate_lda_outputs(lda_model, corpus, dictionary, original_df)
        print("="*80)
        print("所有LDA建模与分析任务完成！请查看输出目录。")
        print("="*80)