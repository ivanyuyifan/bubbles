# ------------------------------------------------------------------
# 使用cntext和DUTIR词典进行细粒度中文情感分析
# ------------------------------------------------------------------
# 安装指南:
# 在您的终端运行: pip install cntext
# ------------------------------------------------------------------

import pandas as pd
import cntext as ct
from tqdm import tqdm

# ==============================================================================
# 1. 参数配置区
# ==============================================================================
# 输入的、已经预处理好的CSV文件路径
INPUT_CSV_PATH = '/Users/fafaya/Desktop/医患关系研究/预处理后语料/weibo_data_cleaned_master.csv'

# 输出带有cntext情感分析结果的新CSV文件路径
OUTPUT_CSV_PATH = '/Users/fafaya/Desktop/医患关系研究/预处理后语料/weibo_data_with_cntext_sentiment.csv'

# ==============================================================================
# 2. 主程序入口
# ==============================================================================
if __name__ == '__main__':
    print("--- 开始使用cntext进行细粒度情感分析任务 ---")

    # --- 加载数据 ---
    try:
        print(f"正在加载文件: {INPUT_CSV_PATH}")
        df = pd.read_csv(INPUT_CSV_PATH)
        df.dropna(subset=['微博内容_清洗后'], inplace=True)
        print(f"成功加载数据，共 {len(df)} 条微博待分析。\n")
    except FileNotFoundError:
        print(f"错误：文件未找到，请检查路径: {INPUT_CSV_PATH}")
        exit()

    # --- 加载情感词典 ---
    print("--- 正在加载DUTIR情感词典 ---")
    # DUTIR词典包含七大类情绪：乐、好、怒、哀、惧、恶、惊
    dutir_dict = ct.load_pkl_dict('DUTIR.pkl')['DUTIR']
    print("词典加载成功！\n")

    # --- 进行情感分析 ---
    print("--- 正在为每条微博计算各类情感词数量 (此过程可能较慢，请耐心等待) ---")

    # 定义一个函数，用于处理单条文本
    def analyze_single_text(text):
        # 使用cntext.sentiment进行分析，返回一个包含各类别计数的字典
        return ct.sentiment(text=str(text), diction=dutir_dict, lang='chinese')

    # 使用tqdm显示进度条
    tqdm.pandas(desc="cntext情感分析中")
    # 对DataFrame的每一行应用分析函数
    sentiment_results = df['微博内容_清洗后'].progress_apply(analyze_single_text)

    # 将返回的字典列表转换为一个DataFrame
    sentiment_df = pd.DataFrame(list(sentiment_results))
    print("\n情感词计数完毕！")
    
    # --- 计算综合情感得分 ---
    print("--- 正在计算综合情感得分 ---")
    # 定义正面和负面情绪类别
    positive_emotions = ['乐_num', '好_num']
    negative_emotions = ['怒_num', '哀_num', '惧_num', '恶_num']

    # 计算总词数，避免除以零的错误
    # sentiment_df['word_num'] 是cntext返回的每条微博的总词数
    total_words = sentiment_df['word_num'].replace(0, 1)

    # 计算正面和负面情感词的占比
    sentiment_df['positive_score'] = sentiment_df[positive_emotions].sum(axis=1) / total_words
    sentiment_df['negative_score'] = sentiment_df[negative_emotions].sum(axis=1) / total_words
    
    # 计算情感净值（正面占比 - 负面占比）
    sentiment_df['net_sentiment_score'] = sentiment_df['positive_score'] - sentiment_df['negative_score']
    print("综合得分计算完毕！")

    # --- 合并结果并保存 ---
    # 将原始DataFrame与情感分析结果的DataFrame按列合并
    final_df = pd.concat([df, sentiment_df], axis=1)

    print("\n情感分析结果预览:")
    # 筛选出一些关键列进行预览
    preview_cols = ['微博内容_清洗后', '乐_num', '怒_num', '哀_num', '好_num', '恶_num', 'net_sentiment_score']
    print(final_df[preview_cols].head())

    try:
        final_df.to_csv(OUTPUT_CSV_PATH, index=False, encoding='utf-8-sig')
        print(f"\n成功！已将带有cntext情感分析结果的数据保存至新文件:\n{OUTPUT_CSV_PATH}")
    except Exception as e:
        print(f"\n错误：保存文件失败: {e}")
        
    print("\n--- cntext情感分析任务全部完成 ---")
