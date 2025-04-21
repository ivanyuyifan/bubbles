library(readr)
library(ggplot2)
library(dplyr)
library(tidytext)

df_word <- read_csv("/Users/fafaya/Desktop/word_freq.csv")

top_words <- df_word %>%
  group_by(来源) %>%
  slice_max(order_by = 频次, n = 20) %>%
  ungroup()

# 使用 reorder_within 按组排序
ggplot(top_words, aes(x = reorder_within(词语, 频次, 来源), y = 频次, fill = 来源)) +
  geom_col(show.legend = FALSE) +
  facet_wrap(~来源, scales = "free_y") +
  coord_flip() +
  scale_x_reordered() +  # 加这一行才能恢复正确的 x 轴标签
  theme_minimal(base_family = "STHeiti") +
  labs(title = "各文本高频词汇前20", x = "词语", y = "频次")


df_pron <- read_csv("/Users/fafaya/Desktop/pronoun_freq.csv")

ggplot(df_pron, aes(x = 代词, y = 频次, fill = 来源)) +
  geom_col(position = "dodge") +
  theme_minimal(base_family = "STHeiti") +
  labs(title = "代词使用频率对比", x = "代词", y = "频次", fill = "文本来源")

