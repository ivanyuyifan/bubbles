import pandas as pd
import re
from datetime import datetime, timedelta
from snownlp import SnowNLP

# 1. 文件路径
input_path = '/Users/fafaya/Desktop/bubbles/医患关系语料库研究/retained_Sina_Comments.xlsx'
output_path = '/Users/fafaya/Desktop/bubbles/医患关系语料库研究/retained_Sina_Comments_with_sentiment.xlsx'

# 2. 读取数据
df = pd.read_excel(input_path)

# 3. 发布时间标准化函数
def parse_time(text):
    today = datetime.today()
    if pd.isna(text):
        return pd.NaT
    text = str(text).strip()

    # 🔍 清洗掉“转赞人数”这类尾缀
    text = re.split(r'[转赞评论].*$', text)[0].strip()

    try:
        # 1) 03月11日 16:45
        if re.match(r"\d{2}月\d{2}日 \d{2}:\d{2}", text):
            dt = datetime.strptime(f"{datetime.today().year}年" + text, "%Y年%m月%d日 %H:%M")
            return dt
        # 2) 今天 12:33
        if re.match(r"今天\s*\d{1,2}:\d{2}", text):
            hour_minute = re.findall(r"\d{1,2}:\d{2}", text)[0]
            return datetime.strptime(today.strftime("%Y-%m-%d") + " " + hour_minute, "%Y-%m-%d %H:%M")
        # 3) x分钟前
        if "分钟前" in text:
            minutes = int(re.findall(r"\d+", text)[0])
            return today - timedelta(minutes=minutes)
        # 4) 2023年10月12日（年月日格式）
        if re.match(r"\d{4}年\d{1,2}月\d{1,2}日", text):
            return datetime.strptime(text, "%Y年%m月%d日")
        return pd.NaT
    except:
        return pd.NaT

# 应用时间转换
df['标准化时间'] = df['发布时间'].apply(parse_time)

# 4. 情感分析打分
def sentiment_score(text):
    if pd.isna(text) or len(str(text).strip()) == 0:
        return None
    return SnowNLP(text).sentiments

df['情感得分'] = df['评论内容'].apply(sentiment_score)

# 5. 提取月份字段（用于趋势图分析）
df['月份'] = df['标准化时间'].dt.to_period('M')

# 6. 保存新文件
df.to_excel(output_path, index=False)
print(f"✅ 情感分析完成，结果保存至：{output_path}")
