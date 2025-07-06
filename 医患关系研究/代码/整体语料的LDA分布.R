# ----------------------------------------------------
# 任务一：医患关系议题的历时性分析 (R语言版 - 修正版)
# ----------------------------------------------------

# 1. 加载必要的包
library(tidyverse)
library(readr)

# --- 参数配置 ---
# 您的主题分布CSV文件路径
csv_file_path <- "/Users/fafaya/Desktop/医患关系研究/final_lda_results/document_topic_distribution.csv"

# =====================================================================
# 关键修正点：创建一个从机器ID到人工命名的“映射”
# =====================================================================
# R的命名向量：`"机器名" = "您想显示的名称"`
# 请确保这里的顺序和内容与您的10个主题完全对应
topic_names_map <- c(
  "Topic_0" = "医疗服务体系建设与优化",
  "Topic_1" = "医患矛盾与个人叙事",
  "Topic_2" = "医学人文与媒介叙事",
  "Topic_3" = "患者就医与治疗流程叙事",
  "Topic_4" = "重大伤医事件的媒介呈现与网络舆论",
  "Topic_5" = "医疗题材言情影视剧集讨论",
  "Topic_6" = "医疗话题的网络暴力与公众情绪冲突",
  "Topic_7" = "特定疾病的病因与治疗探讨",
  "Topic_8" = "医疗领域的法律法规与纠纷处理",
  "Topic_9" = "医疗背景网络小说及其情节讨论"
)


# --- 2. 加载并准备数据 ---
cat("--- 步骤1: 加载LDA主题分布数据 ---\n")
tryCatch({
  weibo_data <- read_csv(csv_file_path)
  cat(sprintf("成功加载数据，共 %d 条记录。\n\n", nrow(weibo_data)))
}, error = function(e) {
  stop(sprintf("错误: 文件加载失败，请检查路径: %s\n%s", csv_file_path, e))
})


# --- 3. 计算年度主题分布 ---
cat("--- 步骤2: 计算各年度主题的平均权重(占比) ---\n")

# 选出所有主题相关的列 (Topic_0, Topic_1, ..., Topic_9)
topic_columns <- names(topic_names_map)

# 按年份分组，并计算每个主题列的平均值
yearly_topic_distribution <- weibo_data %>%
  group_by(年份) %>%
  summarise(across(all_of(topic_columns), mean))

print(yearly_topic_distribution)
cat("\n")


# --- 4. 数据转换与可视化 ---
cat("--- 步骤3: 数据转换与生成可视化图表 ---\n")

# 将宽数据转换为长数据，便于ggplot2绘图
plot_data <- yearly_topic_distribution %>%
  pivot_longer(
    cols = all_of(topic_columns),
    names_to = "Topic_ID", # 列名现在是机器ID，如 "Topic_0"
    values_to = "Weight"
  )

# --- 可视化方案：分面图 (小多图) - 强烈推荐 ---
# 使用 labeller = as_labeller(topic_names_map) 来显示您的命名
plot_faceted <- ggplot(plot_data, aes(x = 年份, y = Weight)) +
  geom_line(aes(group = 1), color = "steelblue", linewidth = 1.2) +
  geom_point(color = "steelblue", size = 3) +
  # 关键一步：使用 labeller 将 Topic_0 等ID转换为您的命名
  facet_wrap(~ Topic_ID, ncol = 5, labeller = as_labeller(topic_names_map)) +
  scale_x_continuous(breaks = unique(plot_data$年份)) +
  labs(
    title = "Evolution of Doctor-Patient Discourse Topics on Weibo (2019-2025)",
    subtitle = "Each panel shows the yearly prevalence of a single topic",
    x = "Year",
    y = "Average Topic Weight (Proportion)"
  ) +
  theme_bw(base_size = 12) +
  theme(
    strip.text = element_text(face = "bold", size = 10), # 让小图标题更清晰
    plot.title = element_text(face = "bold", size = 16),
    plot.subtitle = element_text(size = 12)
  )

# 保存图表
output_filename <- "topic_evolution_faceted_chart_revised.png"
ggsave(output_filename, plot = plot_faceted, width = 18, height = 10, dpi = 300)
cat(sprintf("已成功生成并保存'分面图'至: %s\n", output_filename))


cat("\n所有历时性分析任务已完成！\n")