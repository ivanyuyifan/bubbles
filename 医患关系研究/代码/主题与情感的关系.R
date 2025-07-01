# ------------------------------------------------------------------
# 任务三：分析并可视化主题与情感的关系 (合并数据修正版)
# ------------------------------------------------------------------

# 1. 加载必要的包
library(tidyverse)
library(readr)

# --- 参数配置区 ---

# 文件路径配置
# a. 带有cntext情感分析结果的CSV文件路径
SENTIMENT_DATA_PATH <- "/Users/fafaya/Desktop/医患关系研究/预处理后语料/weibo_data_with_cntext_sentiment.csv"
# b. 带有LDA主题分布结果的CSV文件路径
TOPIC_DATA_PATH <- "/Users/fafaya/Desktop/医患关系研究/final_lda_results/document_topic_distribution.csv"

# 您的主题命名映射
TOPIC_NAMES_MAP <- c(
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


# --- 2. 分别加载两个数据文件 ---
cat("--- 步骤1: 分别加载情感数据和主题数据 ---\n")
tryCatch({
  sentiment_df <- read_csv(SENTIMENT_DATA_PATH)
  topic_df <- read_csv(TOPIC_DATA_PATH)
  cat(sprintf("成功加载情感数据 (%d 条) 和主题数据 (%d 条)。\n\n", nrow(sentiment_df), nrow(topic_df)))
}, error = function(e) {
  stop(sprintf("错误: 文件加载失败，请检查路径。\n%s", e))
})

# --- 3. 合并数据 ---
cat("--- 步骤2: 合并情感与主题数据 ---\n")

# 检查两个文件的行数是否一致，这是合并的前提
if (nrow(sentiment_df) != nrow(topic_df)) {
  stop("错误: 情感数据文件和主题数据文件的行数不一致，无法合并。请检查数据源。")
}

# 选出主题数据中我们需要的Topic列
topic_columns <- names(TOPIC_NAMES_MAP)
topic_probabilities_df <- topic_df %>% select(all_of(topic_columns))

# 使用 bind_cols 按列合并，因为两个文件是基于同一个源生成的，行序一致
merged_df <- bind_cols(sentiment_df, topic_probabilities_df)
cat("数据合并成功！\n\n")


# --- 4. 为每条微博确定主导议题 ---
cat("--- 步骤3: 为每条微博确定主导议题 ---\n")

merged_df$dominant_topic_id <- pmap_chr(merged_df[topic_columns], ~ {
  probs <- c(...)
  names(probs)[which.max(probs)]
})
merged_df$dominant_topic_name <- TOPIC_NAMES_MAP[merged_df$dominant_topic_id]
cat("主导议题确定完毕。\n\n")


# --- 5. 按主导议题分组，计算平均情感得分 ---
cat("--- 步骤4: 计算各主题的平均情感得分 ---\n")

sentiment_by_topic <- merged_df %>%
  filter(!is.na(dominant_topic_name)) %>%
  group_by(dominant_topic_name) %>%
  summarise(
    mean_net_sentiment = mean(net_sentiment_score, na.rm = TRUE),
    post_count = n()
  ) %>%
  arrange(mean_net_sentiment)

print(sentiment_by_topic)
cat("\n")


# --- 6. 可视化结果 ---
cat("--- 步骤5: 生成主题情感得分对比图 ---\n")

plot_sentiment_by_topic <- ggplot(sentiment_by_topic, 
                                  aes(x = reorder(dominant_topic_name, mean_net_sentiment), 
                                      y = mean_net_sentiment, 
                                      fill = mean_net_sentiment)) +
  geom_col() +
  geom_text(aes(label = sprintf("%.3f", mean_net_sentiment)), hjust = -0.2, size = 4) +
  coord_flip() +
  scale_fill_gradient2(low = "tomato", mid = "gray80", high = "steelblue", midpoint = 0.0) +
  labs(
    title = "Average Net Sentiment Score by Topic",
    subtitle = "Comparing the emotional tone of different discourse topics on Weibo",
    x = "Topic",
    y = "Average Net Sentiment Score"
  ) +
  theme_minimal(base_size = 14) +
  theme(
    legend.position = "none",
    plot.title = element_text(face = "bold", size=18),
    axis.text.y = element_text(size=12)
  )

# 保存图表
output_filename <- "sentiment_by_topic_barchart_final.png"
ggsave(output_filename, plot = plot_sentiment_by_topic, width = 16, height = 10, dpi = 300)
cat(sprintf("已成功生成并保存'主题情感得分对比图'至: %s\n", output_filename))

cat("\n所有任务已完成！\n")
