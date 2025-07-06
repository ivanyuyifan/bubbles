# ------------------------------------------------------------------
# Python任务：计算正面/负面情感语料中，各LDA主题的平均占比
# ------------------------------------------------------------------
import pandas as pd
import os

# --- 参数配置区 ---
# 输入文件路径
SENTIMENT_DATA_PATH = '/Users/fafaya/Desktop/医患关系研究/预处理后语料/weibo_data_with_cntext_sentiment.csv'
TOPIC_DATA_PATH = '/Users/fafaya/Desktop/医患关系研究/final_lda_results/document_topic_distribution.csv'

# 输出目录
OUTPUT_DIR = '/Users/fafaya/Desktop/医患关系研究/final_analysis_results/'
# 输出文件名
OUTPUT_FILENAME = 'topic_proportions_by_sentiment.csv'

def aggregate_topic_sentiment():
    """加载、合并数据，并计算各主题在不同情感下的平均权重。"""
    
    print("--- 步骤1: 加载情感数据和主题数据 ---")
    try:
        sentiment_df = pd.read_csv(SENTIMENT_DATA_PATH)
        topic_df = pd.read_csv(TOPIC_DATA_PATH)
        print(f"成功加载情感数据 ({len(sentiment_df)} 条) 和主题数据 ({len(topic_df)} 条)。\n")
    except FileNotFoundError as e:
        print(f"错误: 文件加载失败，请检查路径。 {e}")
        return

    # --- 数据合并 ---
    if len(sentiment_df) != len(topic_df):
        print("错误: 情感数据和主题数据行数不匹配，无法合并。")
        return
        
    topic_columns = [col for col in topic_df.columns if col.startswith('Topic_')]
    merged_df = pd.concat([sentiment_df, topic_df[topic_columns]], axis=1)
    print("数据合并成功！\n")

    # --- 创建子语料库并计算主题平均权重 ---
    print("--- 步骤2: 计算正面/负面语料中的主题平均占比 ---")
    positive_corpus = merged_df[merged_df['net_sentiment_score'] > 0]
    negative_corpus = merged_df[merged_df['net_sentiment_score'] < 0]

    positive_means = positive_corpus[topic_columns].mean().rename('Positive')
    negative_means = negative_corpus[topic_columns].mean().rename('Negative')

    # --- 整理并保存结果 ---
    comparison_df = pd.DataFrame([positive_means, negative_means]).T.reset_index()
    comparison_df.columns = ['Topic_ID', 'Positive_Weight', 'Negative_Weight']
    
    # 确保输出目录存在
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILENAME)
    comparison_df.to_csv(output_path, index=False, encoding='utf-8-sig')
    
    print("计算完成！结果预览：")
    print(comparison_df)
    print(f"\n已将结果保存至: {output_path}")

if __name__ == '__main__':
    aggregate_topic_sentiment()
