import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import warnings
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# 设置路径
save_dir = "/Users/fafaya/Desktop/随机森林/糖尿病预测"
os.makedirs(save_dir, exist_ok=True)

# 中文与图像设置
plt.rcParams['font.sans-serif'] = ['Heiti TC'] 
plt.rcParams['axes.unicode_minus'] = False 
plt.rcParams['savefig.dpi'] = 500
plt.rcParams['figure.dpi'] = 500
warnings.filterwarnings("ignore")

# 读取数据
DataFrame = pd.read_excel('/Users/fafaya/Desktop/随机森林/糖尿病预测/dia.xls')

# 特征映射
feature_map = {
    '年龄': '年龄',
    '高密度脂蛋白胆固醇': '高密度脂蛋白胆固醇',
    '低密度脂蛋白胆固醇': '低密度脂蛋白胆固醇',
    '极低密度脂蛋白胆固醇': '极低密度脂蛋白胆固醇',
    '甘油三酯': '甘油三酯',
    '总胆固醇': '总胆固醇',
    '脉搏': '脉搏',
    '舒张压': '舒张压',
    '高血压史': '高血压史',
    '尿素氮': '尿素氮',
    '尿酸': '尿酸',
    '肌酐': '肌酐',
    '体重检查结果': '体重检查结果'
}

# 绘制多个箱线图并保存
plt.figure(figsize=(15, 10))
for i, (col, col_name) in enumerate(feature_map.items(), 1):
    plt.subplot(3, 5, i)
    sns.boxplot(x=DataFrame['是否糖尿病'], y=DataFrame[col])
    plt.title(f'{col_name}的箱线图', fontsize=14)
    plt.ylabel('数值', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig(f"{save_dir}/特征箱线图.png")
plt.close()

# 删除卡号列
DataFrame.drop(columns=['卡号'], inplace=True)

# 计算相关系数并保存热图
df_corr = DataFrame.corr()
fig = px.imshow(
    df_corr,
    text_auto=True,
    aspect="auto",
    color_continuous_scale='RdBu_r'
)
fig.write_image(f"{save_dir}/特征相关性热图.png", scale=3)

# 构建训练数据集
X = DataFrame.drop(['是否糖尿病', '高密度脂蛋白胆固醇'], axis=1)
y = DataFrame['是否糖尿病']
train_X, test_X, train_y, test_y = train_test_split(X, y, test_size=0.2, random_state=1)

# 随机森林建模
rf_clf = RandomForestClassifier(random_state=15)
rf_clf.fit(train_X, train_y)

# 模型预测与性能评估
pred_y_rf = rf_clf.predict(test_X)
class_report_rf = classification_report(test_y, pred_y_rf)

# 打印并保存分类报告
print(class_report_rf)
with open(f"{save_dir}/模型性能报告.txt", "w") as f:
    f.write(class_report_rf)

# 特征重要性可视化并保存
feature_importances = rf_clf.feature_importances_
features_rf = pd.DataFrame({
    '特征': X.columns,
    '重要度': feature_importances
})
features_rf.sort_values(by='重要度', ascending=False, inplace=True)

plt.figure(figsize=(6, 5))
sns.barplot(x='重要度', y='特征', data=features_rf)
plt.xlabel('重要度')
plt.ylabel('特征')
plt.title('随机森林特征图')
plt.tight_layout()
plt.savefig(f"{save_dir}/随机森林特征图.png")
plt.close()
