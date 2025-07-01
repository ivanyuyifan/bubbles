import matplotlib.pyplot as plt

# 1. 根据您图片中的数据点，手动提取的数据
# X轴：主题数量 (Number of Topics)
x_values = range(2, 16)  # 从2到15

# Y轴：对应的一致性得分 (Coherence Score)
y_values = [
    0.400,  # K=2
    0.400,  # K=3
    0.439,  # K=4
    0.401,  # K=5
    0.434,  # K=6
    0.454,  # K=7
    0.473,  # K=8
    0.488,  # K=9
    0.502,  # K=10 (Peak)
    0.464,  # K=11
    0.450,  # K=12
    0.433,  # K=13
    0.446,  # K=14
    0.478   # K=15
]

# 2. 开始绘图
print("正在重新绘制主题一致性得分曲线...")
# 设置画布大小，使其更清晰
plt.figure(figsize=(12, 7))

# 绘制折线图，并添加标记点以突出每个数据点
plt.plot(x_values, y_values, marker='o', linestyle='-', color='steelblue')

# 3. 设置英文标题和坐标轴标签
plt.title('Topic Coherence Score vs. Number of Topics', fontsize=16)
plt.xlabel('Number of Topics (K)', fontsize=12)
plt.ylabel('Coherence Score (c_v)', fontsize=12)

# 4. 优化图表细节
# 确保X轴的刻度都是整数，与您的原图一致
plt.xticks(x_values)
# 添加网格背景
plt.grid(True)
# 自动调整布局，防止标签重叠
plt.tight_layout()

# 5. 保存图表为高分辨率图片文件
output_filename = 'coherence_curve_english.png'
plt.savefig(output_filename, dpi=300) # dpi=300 保证了图片清晰度，适合放入论文或PPT

print(f"图表已成功重绘，并以英文标签保存为 '{output_filename}'")

# 6. 显示图表 (如果您在Jupyter Notebook等环境中运行，会直接显示)
plt.show()