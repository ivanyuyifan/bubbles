import pandas as pd
import os
import jieba
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# --- 配置区 ---

# 1. 您的预处理后的主文件路径
MASTER_CSV_PATH = '/Users/fafaya/Desktop/医患关系研究/预处理后语料/weibo_data_cleaned_master.csv'

# 2. 停用词文件路径 (请确保该文件存在)
STOPWORDS_PATH = '/Users/fafaya/Desktop/医患关系研究/hit_stopwords.txt' 

# 3. 用于生成词云图的中文字体文件路径 (请根据您的系统修改)
# 对于macOS, 可以在 /System/Library/Fonts/Supplemental/ 路径下找到，如 'PingFang.ttc'
# 对于Windows, 可以在 C:/Windows/Fonts/ 路径下找到，如 'simhei.ttf'
FONT_PATH = '/System/Library/Fonts/PingFang.ttc'

# --- 主分析函数 ---

def generate_descriptive_stats(file_path):
    """
    读取预处理后的数据，并生成一份完整的描述性统计报告。
    """
    print("="*80)
    print("开始生成语料库描述性统计报告...")
    print("="*80)

    # --- 数据加载 ---
    try:
        # 加载数据，并直接将'微博发布时间'列解析为日期时间格式
        df = pd.read_csv(file_path, parse_dates=['微博发布时间'])
        print(f"成功加载文件，共 {len(df)} 条预处理后的微博。\n")
    except FileNotFoundError:
        print(f"错误：文件未找到，请检查路径: {file_path}")
        return
    except Exception as e:
        print(f"加载文件时出错: {e}")
        return

    # --- 1. 语料库总体概览 ---
    print("--- 1. 语料库总体概览 ---")
    total_posts = len(df)
    start_date = df['微博发布时间'].min().strftime('%Y-%m-%d')
    end_date = df['微博发布时间'].max().strftime('%Y-%m-%d')
    total_likes = df['点赞数'].sum()
    total_reposts = df['转发数'].sum()
    total_comments = df['评论数'].sum()
    total_engagement = df['总互动量'].sum()

    print(f"微博总数: {total_posts:,} 条")
    print(f"时间跨度: {start_date} 到 {end_date}")
    print(f"总点赞数: {total_likes:,}")
    print(f"总转发数: {total_reposts:,}")
    print(f"总评论数: {total_comments:,}")
    print(f"总互动量: {total_engagement:,}")
    print(f"平均每条微博互动量: {total_engagement/total_posts:.2f}\n")

    # --- 2. 讨论热度与参与度的历时分布 ---
    print("--- 2. 讨论热度与参与度的历时分布 ---")
    
    # 按年份统计
    posts_per_year = df.groupby('年份').size()
    engagement_per_year = df.groupby('年份')['总互动量'].sum()
    print("各年度发帖数量:")
    print(posts_per_year)
    print("\n各年度总互动量:")
    print(engagement_per_year)

    # 按月份统计
    df_monthly = df.set_index('微博发布时间')
    posts_per_month = df_monthly.resample('M').size()
    
    # 找到发帖量最高的月份
    peak_month_posts = posts_per_month.idxmax()
    print(f"\n讨论热度最高峰出现在: {peak_month_posts.strftime('%Y年%m月')}, 该月共发帖 {posts_per_month.max():,} 条。")
    
    # 可视化月度发帖量
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.figure(figsize=(16, 6))
    posts_per_month.plot(kind='line', title='月度微博发帖量趋势 (2019-2025)', lw=2)
    plt.xlabel('时间')
    plt.ylabel('微博数量')
    plt.savefig('monthly_posts_trend.png')
    print("  -> 已生成并保存月度发帖量趋势图: monthly_posts_trend.png\n")
    # plt.show() # 如果在Jupyter环境中，可以取消这行注释来直接显示图片

    # --- 3. 内容特征分析 ---
    print("--- 3. 内容特征分析 ---")
    # 计算清洗后文本的平均长度
    avg_length = df['微博内容_清洗后'].str.len().mean()
    print(f"平均每条微博（清洗后）长度: {avg_length:.2f} 字符")

    # 找出互动量最高的10条微博
    top_10_posts = df.nlargest(10, '总互动量')[['微博内容', '总互动量', '微博发布时间']]
    print("\n总互动量最高的10条微博:")
    for index, row in top_10_posts.iterrows():
        print(f"  - 互动量: {row['总互动量']:,} ({row['微博发布时间'].strftime('%Y-%m-%d')}) | 内容: {row['微博内容'][:50]}...")
    print("\n")

    # --- 4. 初步文本分析 (高频词与词云) ---
    print("--- 4. 初步文本分析 (高频词与词云) ---")
    try:
        with open(STOPWORDS_PATH, 'r', encoding='utf-8') as f:
            stopwords = [line.strip() for line in f.readlines()]
        print("停用词表加载成功。")

        all_text = ' '.join(df['微博内容_清洗后'].dropna())
        words = [word for word in jieba.lcut(all_text) if word.strip() and word not in stopwords and len(word) > 1]
        
        word_counts = Counter(words)
        top_20_words = word_counts.most_common(20)

        print("\n语料库Top 20高频词 (已去除停用词):")
        for word, count in top_20_words:
            print(f"  - {word}: {count:,} 次")

        # 生成词云图
        wordcloud = WordCloud(
            font_path=FONT_PATH,
            width=1200,
            height=800,
            background_color='white',
            max_words=100
        ).generate_from_frequencies(word_counts)

        plt.figure(figsize=(12, 8))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('高频词词云图')
        plt.savefig('wordcloud.png')
        print("\n  -> 已生成并保存高频词词云图: wordcloud.png\n")
        # plt.show()
    except FileNotFoundError as e:
        print(f"\n警告: 未能进行文本分析，因为找不到文件: {e}")
        print("请确保停用词表和字体文件路径正确。\n")
    except Exception as e:
        print(f"\n文本分析时发生错误: {e}\n")


    # --- 5. [预留] 情感分布分析 ---
    print("--- 5. [预留] 情感分布分析 ---")
    print("此部分需要您先运行情感分析，为DataFrame添加 'sentiment_score' 或 'sentiment_category' 列。")
    # ----------------- 以下是示例代码，请在完成情感分析后再取消注释并运行 -----------------
    # if 'sentiment_category' in df.columns:
    #     sentiment_distribution = df['sentiment_category'].value_counts(normalize=True) * 100
    #     print("\n总体情感分布:")
    #     print(sentiment_distribution)
        
    #     # 可视化情感分布
    #     plt.figure(figsize=(8, 8))
    #     sentiment_distribution.plot(kind='pie', autopct='%.2f%%', title='微博情感总体分布')
    #     plt.ylabel('') # 隐藏y轴标签
    #     plt.savefig('sentiment_distribution_pie_chart.png')
    #     print("\n  -> 已生成并保存情感分布饼图: sentiment_distribution_pie_chart.png")
    #     # plt.show()
    # else:
    #     print("DataFrame中未找到 'sentiment_category' 列，跳过情感分布分析。")

    print("="*80)
    print("描述性统计报告生成完毕！")
    print("="*80)

# ==============================================================================
# 主程序入口
# ==============================================================================
if __name__ == '__main__':
    # 确保停用词和字体文件存在，否则文本分析部分会跳过
    if not os.path.exists(STOPWORDS_PATH):
        print(f"警告: 停用词文件未找到！路径: {STOPWORDS_PATH}")
    if not os.path.exists(FONT_PATH):
        print(f"警告: 字体文件未找到！路径: {FONT_PATH}")
    
    generate_descriptive_stats(MASTER_CSV_PATH)