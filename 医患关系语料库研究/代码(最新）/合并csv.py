import pandas as pd
import os

def preprocess_weibo_data(root_path, output_dir):
    """
    完整的微博数据预处理流程：
    1. 合并所有CSV文件。
    2. 进行格式清洗、去重、内容过滤和特征工程。
    3. 保存一个完整的主文件。
    4. 按年份拆分并保存独立文件。
    """
    # --- 1. 合并所有CSV文件 ---
    all_dfs = []
    for dirpath, _, filenames in os.walk(root_path):
        for filename in filenames:
            if filename.endswith('.csv'):
                file_path = os.path.join(dirpath, filename)
                try:
                    df = pd.read_csv(file_path, encoding='utf-8-sig')
                    all_dfs.append(df)
                except Exception as e:
                    print(f"读取文件 {file_path} 时出错: {e}")
    
    if not all_dfs:
        print("未找到任何CSV文件，程序退出。")
        return

    master_df = pd.concat(all_dfs, ignore_index=True)
    print(f"步骤1: 所有CSV文件合并完毕，共 {len(master_df)} 条原始数据。")

    # --- 2. 格式清洗与转换 ---
    master_df['微博发布时间'] = pd.to_datetime(master_df['微博发布时间'], errors='coerce')
    numeric_cols = ['点赞数', '转发数', '评论数']
    for col in numeric_cols:
        master_df[col] = pd.to_numeric(master_df[col], errors='coerce').fillna(0).astype(int)
    
    # 过滤掉时间转换失败或内容为空的行
    master_df.dropna(subset=['微博发布时间', '微博内容'], inplace=True)
    master_df = master_df[master_df['微博内容'].str.strip() != ''].copy() # 使用 .copy() 避免 SettingWithCopyWarning
    print("步骤2: 格式清洗与转换完毕。")

    # --- 3. 高级去重 (方案B) ---
    # a. 清洗文本内容，用于判断核心内容是否重复
    def clean_text(text):
        if not isinstance(text, str):
            return ""
        text = re.sub(r"http\S+", "", text)
        text = re.sub(r"@[^ ]+", "", text)
        text = re.sub(r"#[^#]+#", "", text)
        return text.strip()
    
    master_df['微博内容_清洗后'] = master_df['微博内容'].apply(clean_text)

    # b. 计算总互动量
    master_df['总互动量'] = master_df['点赞数'] + master_df['转发数'] + master_df['评论数']

    # c. 排序后去重
    initial_rows = len(master_df)
    master_df.sort_values(by=['微博内容_清洗后', '总互动量'], ascending=[True, False], inplace=True)
    master_df.drop_duplicates(subset=['微博内容_清洗后'], keep='first', inplace=True)
    print(f"步骤3: 高级去重完毕。去重前: {initial_rows}条, 去重后: {len(master_df)}条。")

    # --- 4. 特征工程 ---
    master_df['年份'] = master_df['微博发布时间'].dt.year
    master_df['月份'] = master_df['微博发布时间'].dt.month
    print("步骤4: 特征工程完毕。")

    # --- 5. 保存一个完整的主文件 ---
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    master_output_path = os.path.join(output_dir, 'weibo_data_cleaned_master.csv')
    master_df.to_csv(master_output_path, index=False, encoding='utf-8-sig')
    print(f"步骤5: 完整的预处理后主文件已保存至: {master_output_path}")

    # --- 6. 按年份拆分并保存独立文件 ---
    unique_years = sorted(master_df['年份'].unique())
    for year in unique_years:
        year_df = master_df[master_df['年份'] == year]
        year_output_path = os.path.join(output_dir, f'weibo_data_{year}.csv')
        year_df.to_csv(year_output_path, index=False, encoding='utf-8-sig')
        print(f"  -> 已保存 {year} 年的数据，共 {len(year_df)} 条，路径: {year_output_path}")
    
    print("步骤6: 按年份拆分保存完毕。所有预处理工作完成！")

# --- 使用示例 ---
import re
# 假设您的原始语料路径和希望的输出路径如下
raw_corpus_path = '/Users/fafaya/Desktop/医患关系研究/语料'
processed_output_path = '/Users/fafaya/Desktop/医患关系研究/预处理后语料'

preprocess_weibo_data(raw_corpus_path, processed_output_path)