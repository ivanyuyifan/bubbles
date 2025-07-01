# ------------------------------------------------------------------
# 使用PaddleNLP进行高精度中文情感分析 (更换模型核心版)
# ------------------------------------------------------------------

import pandas as pd
from paddlenlp import Taskflow
from tqdm import tqdm
import os

# ==============================================================================
# 1. 参数配置区
# ==============================================================================
# 输入的、已经预处理好的CSV文件路径
INPUT_CSV_PATH = '/Users/fafaya/Desktop/医患关系研究/预处理后语料/weibo_data_cleaned_master.csv'

# 输出带有新情感分析结果的CSV文件路径
OUTPUT_CSV_PATH = '/Users/fafaya/Desktop/医患关系研究/预处理后语料/weibo_data_with_paddlenlp_sentiment.csv'

# ==============================================================================
# 2. 初始化情感分析模型
# ==============================================================================
# 首次运行时，程序会自动下载新的预训练模型，请确保网络连接正常。
try:
    print("--- 正在初始化PaddleNLP情感分析模型 (首次运行需要下载新模型，请稍候)... ---")
    
    # *** 最终修正点 ***
    # 我们明确指定使用 'skep_ernie_1.0_large_ch_senta' 这个强大的情感分析模型。
    # 它的内部机制与默认模型不同，有望解决之前的兼容性问题。
    senta = Taskflow(
        "sentiment_analysis", 
        model="skep_ernie_1.0_large_ch_senta", 
        schema=['正面', '负面']
    )
    
    print("模型初始化成功！\n")
except Exception as e:
    print(f"模型初始化失败，请检查网络连接或paddlenlp/paddlepaddle安装。错误: {e}")
    exit()

# ==============================================================================
# 3. 主程序入口
# ==============================================================================
if __name__ == '__main__':
    print(f"当前运行环境的Python路径: {os.sys.executable}")

    print("\n--- 开始进行高精度情感分析任务 ---")
    
    # --- 加载数据 ---
    try:
        print(f"正在加载文件: {INPUT_CSV_PATH}")
        df = pd.read_csv(INPUT_CSV_PATH)
        df.dropna(subset=['微博内容_清洗后'], inplace=True)
        print(f"成功加载数据，共 {len(df)} 条微博待分析。\n")
    except FileNotFoundError:
        print(f"错误：文件未找到，请检查路径: {INPUT_CSV_PATH}")
        exit()

    # --- 进行情感分析 ---
    print("--- 正在为每条微博计算情感倾向 (此过程可能较慢，请耐心等待) ---")
    
    batch_size = 16 # 对于大模型，可以适当减小批次大小
    results = []
    texts_to_analyze = df['微博内容_清洗后'].tolist()
    
    for i in tqdm(range(0, len(texts_to_analyze), batch_size), desc="情感分析中"):
        batch_texts = texts_to_analyze[i:i + batch_size]
        try:
            results.extend(senta(batch_texts))
        except Exception as batch_error:
            print(f"在处理批次 {i//batch_size} 时发生错误: {batch_error}")
            placeholder_result = [{'label': '未知', 'score': 0.5}] * len(batch_texts)
            results.extend(placeholder_result)
        
    print("\n情感分析计算完毕！")

    # --- 整理并合并结果 ---
    df['paddlenlp_label'] = [res.get('label', '未知') for res in results]
    df['paddlenlp_score'] = [res.get('score', 0.5) for res in results]
    
    def normalize_score(row):
        if row['paddlenlp_label'] == '负面':
            return 1 - row['paddlenlp_score']
        else:
            return row['paddlenlp_score']

    df['paddlenlp_unified_score'] = df.apply(normalize_score, axis=1)

    # --- 查看结果预览 ---
    print("\n情感分析结果预览:")
    print(df[['微博内容_清洗后', 'paddlenlp_label', 'paddlenlp_unified_score']].head())
    
    print("\n新模型分析出的各情感类别数量统计:")
    print(df['paddlenlp_label'].value_counts())
    
    # --- 保存结果 ---
    try:
        df.to_csv(OUTPUT_CSV_PATH, index=False, encoding='utf-8-sig')
        print(f"\n成功！已将带有新情感分析结果的数据保存至新文件:\n{OUTPUT_CSV_PATH}")
    except Exception as e:
        print(f"\n错误：保存文件失败: {e}")
        
    print("\n--- 高精度情感分析任务全部完成 ---")
