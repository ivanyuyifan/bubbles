import pandas as pd
from snownlp import SnowNLP
from tqdm import tqdm

# ==============================================================================
# 1. 参数配置区
# ==============================================================================
# 输入的、已经预处理好的CSV文件路径
INPUT_CSV_PATH = '/Users/fafaya/Desktop/医患关系研究/预处理后语料/weibo_data_cleaned_master.csv'

# 输出带有情感分数的新CSV文件路径
OUTPUT_CSV_PATH = '/Users/fafaya/Desktop/医患关系研究/预处理后语料/weibo_data_with_sentiment.csv'

# 用于情感分类的阈值
POSITIVE_THRESHOLD = 0.6
NEGATIVE_THRESHOLD = 0.4

# ==============================================================================
# 2. 主分析函数
# ==============================================================================

def analyze_sentiment(df):
    """
    对DataFrame中的每一条微博进行情感分析，并添加情感得分和情感类别列。
    """
    
    def get_sentiment_score(text):
        """计算单条文本的情感得分"""
        try:
            # SnowNLP需要处理字符串
            return SnowNLP(str(text)).sentiments
        except:
            # 如果出现任何错误（例如文本为空或格式问题），返回中性值0.5
            return 0.5

    def get_sentiment_category(score):
        """根据得分返回情感类别"""
        if score > POSITIVE_THRESHOLD:
            return 'Positive'
        elif score < NEGATIVE_THRESHOLD:
            return 'Negative'
        else:
            return 'Neutral'

    # 使用tqdm来显示情感分析的进度条
    tqdm.pandas(desc="正在计算情感得分")
    
    # 对'微博内容_清洗后'列的每一行应用情感分析函数，生成新列'sentiment_score'
    df['sentiment_score'] = df['微博内容_清洗后'].progress_apply(get_sentiment_score)
    
    # 根据情感得分，生成情感类别列'sentiment_category'
    df['sentiment_category'] = df['sentiment_score'].apply(get_sentiment_category)
    
    return df

# ==============================================================================
# 3. 主程序入口
# ==============================================================================
if __name__ == '__main__':
    print("--- 开始进行情感分析任务 ---")
    
    # --- 加载数据 ---
    try:
        print(f"正在加载文件: {INPUT_CSV_PATH}")
        weibo_df = pd.read_csv(INPUT_CSV_PATH)
        weibo_df.dropna(subset=['微博内容_清洗后'], inplace=True)
        print(f"成功加载数据，共 {len(weibo_df)} 条微博待分析。\n")
    except FileNotFoundError:
        print(f"错误：文件未找到，请检查路径: {INPUT_CSV_PATH}")
        exit()

    # --- 进行情感分析 ---
    print("--- 正在为每条微博计算情感得分 (此过程可能需要较长时间，请耐心等待) ---")
    df_with_sentiment = analyze_sentiment(weibo_df)
    print("\n情感分析计算完毕！")

    # --- 查看结果预览 ---
    print("\n情感分析结果预览:")
    print(df_with_sentiment[['微博内容_清洗后', 'sentiment_score', 'sentiment_category']].head())
    
    print("\n各情感类别数量统计:")
    print(df_with_sentiment['sentiment_category'].value_counts())
    
    # --- 保存结果 ---
    try:
        df_with_sentiment.to_csv(OUTPUT_CSV_PATH, index=False, encoding='utf-8-sig')
        print(f"\n成功！已将带有情感分析结果的数据保存至新文件:\n{OUTPUT_CSV_PATH}")
    except Exception as e:
        print(f"\n错误：保存文件失败: {e}")
        
    print("\n--- 情感分析任务全部完成 ---")