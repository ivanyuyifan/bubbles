import pandas as pd
import os

# --- 配置区 ---

# 您的预处理后的主文件路径
MASTER_CSV_PATH = '/Users/fafaya/Desktop/医患关系研究/预处理后语料/weibo_data_cleaned_master.csv'

# 要统计的列名
COLUMN_TO_COUNT = '微博内容_清洗后'

# --- 主程序 ---
def count_total_characters(file_path, column_name):
    """
    读取CSV文件，并统计指定列的总字符数。
    """
    print("="*60)
    print("开始统计语料库总字符数...")
    print("="*60)

    # --- 数据加载 ---
    try:
        print(f"正在加载文件: {file_path}")
        df = pd.read_csv(file_path)
        print(f"成功加载文件，共 {len(df)} 条微博记录。\n")
    except FileNotFoundError:
        print(f"错误：文件未找到，请检查路径: {file_path}")
        return
    except Exception as e:
        print(f"加载文件时出错: {e}")
        return

    # --- 检查列是否存在 ---
    if column_name not in df.columns:
        print(f"错误：在文件中找不到名为 '{column_name}' 的列。")
        print(f"可用的列有: {list(df.columns)}")
        return

    # --- 计算总字符数 ---
    # 首先，确保列中的所有内容都是字符串，并处理可能的空值(NaN)
    df[column_name] = df[column_name].astype(str).fillna('')
    
    # 使用 .str.len() 计算每行的字符长度，然后用 .sum() 求和
    total_characters = df[column_name].str.len().sum()

    # --- 打印结果 ---
    print("--- 统计结果 ---")
    print(f"语料库文件: {os.path.basename(file_path)}")
    print(f"分析列名: '{column_name}'")
    print(f"总字符数 (Total Characters): {total_characters:,}") # 使用:,格式化数字，方便阅读
    print("="*60)


if __name__ == '__main__':
    count_total_characters(MASTER_CSV_PATH, COLUMN_TO_COUNT)

