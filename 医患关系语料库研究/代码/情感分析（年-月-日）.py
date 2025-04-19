import pandas as pd
import re
from datetime import datetime, timedelta
from snownlp import SnowNLP

# 1. 文件路径
input_path = '/Users/fafaya/Desktop/bubbles/医患关系语料库研究/retained_Sina_Comments（筛选后的）.xlsx'
output_path = '/Users/fafaya/Desktop/bubbles/retained_Sina_Comments_with_sentiment(year-month-day).xlsx'

# 2. 读取数据
df = pd.read_excel(input_path)

# 3. 发布时间标准化函数（返回 datetime 类型）
def parse_time(text):
    today = datetime.today()
    if pd.isna(text):
        return pd.NaT
    text = str(text).strip()

    # 🔍 清洗掉“转赞人数”这类尾缀
    text = re.split(r'[转赞评论].*$', text)[0].strip()

    try:
        if re.match(r"\d{2}月\d{2}日 \d{2}:\d{2}", text):
            dt = datetime.strptime(f"{today.year}年" + text, "%Y年%m月%d日 %H:%M")
            return dt
        if re.match(r"今天\s*\d{1,2}:\d{2}", text):
            hm = re.findall(r"\d{1,2}:\d{2}", text)[0]
            return datetime.strptime(today.strftime("%Y-%m-%d") + " " + hm, "%Y-%m-%d %H:%M")
        if "分钟前" in text:
            minutes = int(re.findall(r"\d+", text)[0])
            return today - timedelta(minutes=minutes)
        if re.match(r"\d{4}年\d{1,2}月\d{1,2}日", text):
            return datetime.strptime(text, "%Y年%m月%d日")
        return pd.NaT
    except:
        return pd.NaT

# 4. 应用转换，得到 datetime 类型
df['标准化时间'] = df['发布时间'].apply(parse_time)

# 5. 生成“标准化日期”列（字符串格式：YYYY-MM-DD）
df['标准化日期'] = df['标准化时间'].dt.strftime('%Y-%m-%d')

# 6. 情感打分（SnowNLP）
def sentiment_score(text):
    if pd.isna(text) or len(str(text).strip()) == 0:
        return None
    return SnowNLP(text).sentiments

df['情感得分'] = df['评论内容'].apply(sentiment_score)

# 7. 保存结果
df.to_excel(output_path, index=False)
print(f"✅ 情感分析完成，输出文件路径：{output_path}")
print("📅 日期已标准化为 YYYY-MM-DD 格式，情感得分列已添加")
