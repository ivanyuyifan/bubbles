library(readr)
library(dplyr)
library(ggplot2)

df_emo <- read_csv("/Users/fafaya/Desktop/情绪词频统计.csv")

df_summary <- df_emo %>%
  group_by(来源, 情绪类型) %>%
  summarise(总频次 = sum(频次), .groups = "drop")

ggplot(df_summary, aes(x = 情绪类型, y = 总频次, fill = 来源)) +
  geom_col(position = "dodge") +
  theme_minimal(base_family = "STHeiti") +
  labs(title = "正向 / 负向 情绪词使用频率", x = "情绪类别", y = "频次", fill = "文本来源")

df_top_words <- df_emo %>%
  group_by(来源) %>%
  slice_max(order_by = 频次, n = 10)

ggplot(df_top_words, aes(x = reorder_within(情绪词, 频次, 来源), y = 频次, fill = 来源)) +
  geom_col(show.legend = FALSE) +
  facet_wrap(~来源, scales = "free_y") +
  coord_flip() +
  scale_x_reordered() +
  theme_minimal(base_family = "STHeiti") +
  labs(title = "各文本高频情绪词TOP", x = "情绪词", y = "频次")
