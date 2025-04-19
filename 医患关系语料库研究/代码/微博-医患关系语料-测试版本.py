import pandas as pd
import re

# 1. 读取原始数据
file_path = '/Users/fafaya/Desktop/Sina Visitor System.xlsx'
df = pd.read_excel(file_path)

# 2. 删除空内容、去重
df = df[df['评论内容'].notnull()]
df = df.drop_duplicates(subset='评论内容')
df.reset_index(drop=True, inplace=True)

# 3. 自定义清洗函数（去除表情、标点等）
def clean_text(text):
    if pd.isna(text):
        return ''
    text = str(text)
    text = re.sub(r"\[.*?\]", "", text)  # 去除微博表情 [doge]
    text = re.sub(r"[！？!~—…「」『』【】★◆■●▼▽▲→←↓↑•※☆◎◆◇¤￥@#%^&*_+=|\\<>《》【】\[\]{}“”‘’]", "", text)
    text = re.sub(r"[!！。,.，]{2,}", "", text)  # 重复标点
    text = re.sub(r"\s+", " ", text).strip()   # 多余空格
    return text

# 4. 应用清洗
df['评论内容'] = df['评论内容'].apply(clean_text)

# 5. 过滤无关关键词
irrelevant_keywords = ['电视剧', '剧情', '饰演', '主演', '热播', '追剧', '剧情片', '改编', '荧幕', '演绎']
df = df[~df['评论内容'].str.contains('|'.join(irrelevant_keywords), na=False)]

# 6. 设置关键词列表
direct_keywords = ['医患关系', '医患纠纷', '医患冲突', '医患沟通', '医患信任', '医生患者', '病人医生']
medical_keywords = ['医生', '患者', '病人', '医护', '护士', '中医', '专家', '主任', '主治医',
                    '实习医生', '医院', '门诊', '诊所', '病房', 'ICU', '手术', '治疗', '输液', 
                    '打针', '检查', '复查', '开药', '会诊', '问诊', '住院', '挂号', '体检']
emotional_keywords = ['沟通', '信任', '感谢', '感动', '耐心', '温柔', '认真', '负责', '专业',
                      '态度差', '敷衍', '不理', '吼我', '投诉', '忽视', '不耐烦', '吓人']

# 7. 打标签
def keyword_match(text, keyword_list):
    return any(keyword in text for keyword in keyword_list)

df['是否直接相关'] = df['评论内容'].apply(lambda x: keyword_match(x, direct_keywords))
df['是否提及医疗主体'] = df['评论内容'].apply(lambda x: keyword_match(x, medical_keywords))
df['是否包含情感词'] = df['评论内容'].apply(lambda x: keyword_match(x, emotional_keywords))

# 8. 综合判断是否保留（任一为 True 即保留）
df['是否保留'] = df[['是否直接相关', '是否提及医疗主体', '是否包含情感词']].any(axis=1)

# 9. 筛选保留评论
retained_df = df[df['是否保留']]

# 10. 保存完整数据（含标签）和筛选结果
df.to_excel('/Users/fafaya/Desktop/cleaned_Sina_Comments_all.xlsx', index=False)
retained_df.to_excel('/Users/fafaya/Desktop/retained_Sina_Comments.xlsx', index=False)

print(f"处理完成！共评论数：{len(df)}，其中保留：{len(retained_df)} 条")
print("✅ 全部数据含标签保存在：cleaned_Sina_Comments_all.xlsx")
print("✅ 筛选后的评论保存在：retained_Sina_Comments.xlsx")
