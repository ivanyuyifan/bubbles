library(readr)
library(dplyr)
library(ggplot2)
library(tidytext)
library(scales)

# 读取关键词结果
keywords <- read_csv("/Users/fafaya/Desktop/关键词提取_TFIDF_TextRank.csv")

# 筛选 Top 15（按来源和方法分组）
top_keywords <- keywords %>%
  group_by(来源, 方法) %>%
  slice_max(order_by = 权重, n = 15) %>%
  ungroup()

# 画图：关键词权重柱状图
ggplot(top_keywords, aes(x = reorder_within(关键词, 权重, list(来源, 方法)), 
                         y = 权重, fill = 方法)) +
  geom_col(show.legend = TRUE) +
  facet_grid(来源 ~ 方法, scales = "free") +
  coord_flip() +
  scale_x_reordered() +
  scale_fill_manual(values = c("#EF476F", "#118AB2")) +
  theme_minimal(base_size = 14, base_family = "STHeiti") +
  labs(
    title = "TF-IDF & TextRank 关键词对比图",
    x = "关键词",
    y = "权重",
    fill = "提取方法"
  )
