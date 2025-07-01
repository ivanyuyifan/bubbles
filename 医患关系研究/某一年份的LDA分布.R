# ------------------------------------------------------------------
# 任务：按月份分析特定年份的主题演变趋势 (R语言版)
# ------------------------------------------------------------------

# 1. 加载必要的包
library(tidyverse)
library(readr)

# --- 参数配置区 ---

# 您可以修改这里的年份，来分析任何您感兴趣的年份
TARGET_YEAR <- 2020

# 您的主题分布CSV文件路径
CSV_FILE_PATH <- "/Users/fafaya/Desktop/医患关系研究/final_lda_results/document_topic_distribution.csv"

# 再次定义您的主题命名映射，确保图表标签正确
# (这是我们之前确定的版本，您可以根据需要调整)
TOPIC_NAMES_MAP <- c(
  "Topic_0" = "医疗服务体系建设与优化",
  "Topic_1" = "医患矛盾与个人叙事",
  "Topic_2" = "医学人文与媒介叙事",
  "Topic_3" = "患者就医与治疗流程叙事",
  "Topic_4" = "重大伤医事件的媒介呈现与网络舆论",
  "Topic_5" = "医疗题材言情小说/剧集讨论",
  "Topic_6" = "饭圈文化与医疗领域的冲突事件",
  "Topic_7" = "特定疾病的病因与治疗探讨",
  "Topic_8" = "医疗领域的法律法规与纠纷处理",
  "Topic_9" = "医疗题材网络小说及其情节讨论"
)


# --- 2. 加载并筛选数据 ---
cat(sprintf("--- 步骤1: 加载数据并筛选出 %d 年的数据 ---\n", TARGET_YEAR))
tryCatch({
  weibo_data <- read_csv(CSV_FILE_PATH) %>%
    filter(年份 == TARGET_YEAR) # 筛选出目标年份
  
  if (nrow(weibo_data) == 0) {
    stop(sprintf("错误: 在数据中找不到 %d 年的记录。", TARGET_YEAR))
  }
  
  cat(sprintf("成功加载并筛选出 %d 年的数据，共 %d 条记录。\n\n", TARGET_YEAR, nrow(weibo_data)))
}, error = function(e) {
  stop(sprintf("错误: 文件加载或筛选失败，请检查路径和数据内容。\n%s", e))
})


# --- 3. 计算月度主题分布 ---
cat(sprintf("--- 步骤2: 计算 %d 年各月份主题的平均权重(占比) ---\n", TARGET_YEAR))

# 选出所有主题相关的列
topic_columns <- names(TOPIC_NAMES_MAP)

# 按月份分组，并计算每个主题列的平均值
monthly_topic_distribution <- weibo_data %>%
  group_by(月份) %>%
  summarise(across(all_of(topic_columns), mean))

# 打印结果表格，方便查看
print(as.data.frame(monthly_topic_distribution))
cat("\n")


# --- 4. 数据转换与可视化 ---
cat("--- 步骤3: 数据转换与生成可视化图表 ---\n")

# 将宽数据转换为长数据，便于ggplot2绘图
plot_data_monthly <- monthly_topic_distribution %>%
  pivot_longer(
    cols = all_of(topic_columns),
    names_to = "Topic_ID",
    values_to = "Weight"
  )

# --- 使用分面图进行可视化 ---
plot_monthly_faceted <- ggplot(plot_data_monthly, aes(x = 月份, y = Weight)) +
  geom_line(aes(group = 1), color = "steelblue", linewidth = 1) +
  geom_point(color = "steelblue", size = 2.5) +
  # 关键一步：使用 labeller 将 Topic_0 等ID转换为您的命名
  facet_wrap(~ Topic_ID, ncol = 5, labeller = as_labeller(TOPIC_NAMES_MAP)) +
  scale_x_continuous(breaks = 1:12) + # 确保X轴显示1到12月
  labs(
    title = sprintf("Monthly Evolution of Topics for Year %d", TARGET_YEAR),
    subtitle = "The chart shows the monthly prevalence of each of the 10 topics",
    x = "Month",
    y = "Average Topic Weight (Proportion)"
  ) +
  theme_bw(base_size = 12) +
  theme(
    strip.text = element_text(face = "bold", size = 9), # 调整小图标题大小以适应更多图
    plot.title = element_text(face = "bold", size = 16)
  )

# 保存图表
output_filename <- sprintf("topic_evolution_%d_monthly.png", TARGET_YEAR)
ggsave(output_filename, plot = plot_monthly_faceted, width = 18, height = 10, dpi = 300)
cat(sprintf("已成功生成并保存'%d年月度主题演变图'至: %s\n", TARGET_YEAR, output_filename))


cat("\n所有月度分析任务已完成！\n")