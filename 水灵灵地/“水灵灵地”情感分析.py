import pandas as pd
from snownlp import SnowNLP
import matplotlib.pyplot as plt
from matplotlib import cm

# 读取 Excel 数据
filepath = "/Users/fafaya/Desktop/bubbles/水灵灵地/水灵灵地词频与搭配_results.xlsx"
df = pd.read_excel(filepath, sheet_name="Bigram Association")

# 定义情感分析函数（剔除"水灵灵地"）
def analyze_sentiment_without_target(bigram, target="水灵灵地"):
    try:
        # 去掉 "水灵灵地" 并保留搭配词
        other_words = bigram.replace(target, "").strip()
        if other_words:  # 确保剩余内容非空
            s = SnowNLP(other_words)
            return s.sentiments  # 返回情感得分
        else:
            return None  # 如果去掉后为空，返回 None
    except Exception as e:
        print(f"Error analyzing sentiment for: {bigram}, Error: {e}")
        return None

#这边定义了大于0.6的是积极，小于0.4的是消极，位于两者之间的是中立
def classify_sentiment(score):
    if score is None:
        return "Unknown"
    elif score > 0.6:
        return "Positive"
    elif score < 0.4:
        return "Negative"
    else:
        return "Neutral"

# 对 Bigram 列的内容进行情感分析
df["Sentiment Score"] = df["Bigram"].apply(lambda x: analyze_sentiment_without_target(x))
df["Sentiment Label"] = df["Sentiment Score"].apply(classify_sentiment)

# 保存结果到 Excel
output_path = "/Users/fafaya/Desktop/bubbles/水灵灵地/情感分析_SnowNLP.xlsx"
df.to_excel(output_path, index=False)
print(f"情感分析结果已保存到: {output_path}")

# 统计 Sentiment Label 的分布
sentiment_counts = df["Sentiment Label"].value_counts()

# 指定蓝色色值
colors = ['#ADD8E6', '#4682B4', '#1E90FF', 'gray']  # 蓝色系和灰色对应情感分类
labels = ['Positive', 'Neutral', 'Negative', 'Unknown']  # 图例对应的标签

# 绘制饼图
plt.figure(figsize=(8, 6))
wedges, texts, autotexts = plt.pie(
    sentiment_counts,
    labels=sentiment_counts.index,  # 显示情感分类名称
    autopct='%1.1f%%',
    startangle=140,
    colors=colors
)

# 添加图例
plt.legend(
    wedges,  # 对应饼图的每一块
    labels,  # 图例标签
    title="Sentiment Types",  # 图例标题
    loc="center left",  # 图例位置
    bbox_to_anchor=(1, 0, 0.5, 1)  # 调整图例位置
)

# 添加标题
plt.title("Sentiment Label Distribution")

# 保存图表
plt.savefig("/Users/fafaya/Desktop/bubbles/水灵灵地/情感分布饼图.png")
plt.show()