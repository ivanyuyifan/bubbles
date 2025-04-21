import pandas as pd
import jieba
from collections import Counter

# 读取情绪词典
emotion_dict = pd.read_csv('/Users/fafaya/Desktop/emotion_dict.csv')
emotion_map = dict(zip(emotion_dict['词语'], emotion_dict['情绪类型']))

# 输入文本路径
files = {
    "/Users/fafaya/Desktop/宫老师的两封情书.txt": "情书",
    "/Users/fafaya/Desktop/宫老师的后期小作文.txt": "后期小作文"
}

results = []

for path, label in files.items():
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()

    words = jieba.lcut(text)
    emo_counts = Counter([w for w in words if w in emotion_map])

    for word, count in emo_counts.items():
        results.append({
            "来源": label,
            "情绪词": word,
            "频次": count,
            "情绪类型": emotion_map[word]
        })

# 保存结果
df_emo = pd.DataFrame(results)
df_emo.to_csv("/Users/fafaya/Desktop/情绪词频统计.csv", index=False, encoding="utf-8-sig")
print("✅ 情绪词频统计完成，已保存为：情绪词频统计.csv")
