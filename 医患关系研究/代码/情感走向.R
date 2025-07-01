# ------------------------------------------------------------------
# 高级分析：情感/议题历时性演变与关键年份深度剖析
# ------------------------------------------------------------------

# 1. 加载必要的包
library(tidyverse)
library(readr)
library(lubridate)
library(patchwork) # 用于组合多张图

# --- 参数配置区 ---

# 您带有cntext情感分析结果的CSV文件路径
CNTEXT_DATA_PATH <- "/Users/fafaya/Desktop/医患关系研究/预处理后语料/weibo_data_with_cntext_sentiment.csv"

# --- 2. 加载数据 ---
cat("--- 步骤1: 加载带有cntext情感分数的数据 ---\n")
tryCatch({
  weibo_df <- read_csv(CNTEXT_DATA_PATH) %>%
    mutate(微博发布时间 = ymd_hm(微博发布时间, tz = "Asia/Shanghai"))
  
  cat(sprintf("成功加载数据，共 %d 条记录。\n\n", nrow(weibo_df)))
}, error = function(e) {
  stop(sprintf("错误: 文件加载失败，请检查路径: %s\n%s", CNTEXT_DATA_PATH, e))
})


# --- 3. 聚合月度数据 ---
cat("--- 步骤2: 正在分析并聚合月度情感数据... ---\n")

monthly_trend_data <- weibo_df %>%
  mutate(year_month = floor_date(微博发布时间, "month")) %>%
  filter(!is.na(year_month)) %>%
  group_by(year_month) %>%
  summarise(
    mean_net_sentiment = mean(net_sentiment_score, na.rm = TRUE),
    post_count = n()
  )

if (nrow(monthly_trend_data) == 0) {
  stop("错误: 按月份聚合后没有可用于绘图的数据。")
}
cat("数据聚合成功！\n\n")

# ==============================================================================
# 任务一: 绘制带有趋势线的“情感心电图”
# ==============================================================================
cat("--- 任务一: 正在绘制带有趋势线的组合图... ---\n")

# 图一：月度讨论热度图 (带趋势线)
plot_volume_with_trend <- ggplot(monthly_trend_data, aes(x = year_month, y = post_count)) +
  geom_col(fill = "lightblue", alpha = 0.6) +
  # 新增：添加平滑趋势曲线 (loess方法)
  geom_smooth(method = "loess", aes(color = "Trend"), se = FALSE, span = 0.3) +
  scale_color_manual(name = "", values = c("Trend" = "darkblue")) +
  labs(
    title = "A. Monthly Discussion Volume with Trend",
    x = NULL,
    y = "Post Count"
  ) +
  theme_bw(base_size = 14) +
  theme(axis.text.x = element_blank(), legend.position = "top")

# 图二：月度情感净值波动图 (带趋势线)
plot_sentiment_with_trend <- ggplot(monthly_trend_data, aes(x = year_month, y = mean_net_sentiment)) +
  geom_line(color = "tomato", linewidth = 1) +
  # 新增：添加平滑趋势曲线
  geom_smooth(method = "loess", aes(color = "Trend"), se = FALSE, span = 0.3) +
  geom_hline(yintercept = 0, linetype="dashed", color = "gray40") +
  scale_color_manual(name = "", values = c("Trend" = "darkred")) +
  labs(
    title = "B. Monthly Net Sentiment Score with Trend",
    x = "Date (Year)",
    y = "Average Net Sentiment"
  ) +
  theme_bw(base_size = 14) +
  theme(legend.position = "top")

# 组合图表
final_plot_with_trend <- plot_volume_with_trend / plot_sentiment_with_trend + 
  plot_layout(heights = c(1, 1)) +
  plot_annotation(
    title = 'Emotional Pulse of Doctor-Patient Discourse on Weibo (2019-2025)',
    subtitle = 'Blue/Red lines represent smoothed trends (LOESS)',
    theme = theme(plot.title = element_text(face = "bold", size = 20))
  )

# 保存图表
output_filename1 <- "sentiment_pulse_chart_with_trends.png"
ggsave(output_filename1, plot = final_plot_with_trend, width = 16, height = 10, dpi = 300)
cat(sprintf("已成功生成并保存'带趋势线的情感心电图'至: %s\n\n", output_filename1))


# ==============================================================================
# 任务二: 单独绘制并对比2020年和2024年的情感走向
# ==============================================================================
cat("--- 任务二: 正在绘制2020年与2024年的情感走向对比图... ---\n")

# 筛选出2020年和2024年的数据
case_study_data <- weibo_df %>%
  filter(年份 %in% c(2020, 2024)) %>%
  group_by(年份, 月份) %>%
  summarise(mean_net_sentiment = mean(net_sentiment_score, na.rm = TRUE), .groups = 'drop')

# 使用分面图进行对比
plot_case_study <- ggplot(case_study_data, aes(x = 月份, y = mean_net_sentiment)) +
  geom_line(aes(group = 1), color = "tomato", linewidth = 1.2) +
  geom_point(color = "tomato", size = 3) +
  # 在0线处添加一条虚线
  geom_hline(yintercept = 0, linetype="dashed", color = "gray40") +
  # 按年份分面
  facet_wrap(~ 年份) +
  scale_x_continuous(breaks = 1:12) +
  labs(
    title = "Case Study: Monthly Sentiment Trends in Critical Years",
    subtitle = "Comparing sentiment evolution during 2020 (COVID-19 Outbreak) and 2024 (Dr. Li Incident)",
    x = "Month",
    y = "Average Net Sentiment Score"
  ) +
  theme_bw(base_size = 14) +
  theme(
    plot.title = element_text(face = "bold", size = 18),
    strip.text = element_text(face = "bold", size = 14)
  )

# 保存图表
output_filename2 <- "case_study_2020_vs_2024.png"
ggsave(output_filename2, plot = plot_case_study, width = 16, height = 7, dpi = 300)
cat(sprintf("已成功生成并保存'关键年份对比图'至: %s\n", output_filename2))

cat("\n所有分析任务已完成！\n")
