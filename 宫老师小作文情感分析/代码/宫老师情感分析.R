library(readr)
library(ggplot2)
library(dplyr)

# 读取数据
df <- read_csv("/Users/fafaya/Desktop/宫老师_情感分析_by_sentence.csv")


# ✅ 方法一：情绪趋势平滑图（geom_smooth()） --------------------------------------------

ggplot(df, aes(x = 句号, y = 情感得分, color = 来源)) +
  geom_smooth(method = "loess", span = 0.3, se = FALSE, size = 1.5, alpha = 0.8) +
  theme_minimal(base_size = 14, base_family = "STHeiti") +
  scale_color_manual(values = c("#D7263D", "#1B9AAA")) +
  labs(
    title = "文本情绪趋势曲线（平滑）",
    x = "句子编号",
    y = "情感得分",
    color = "文本来源"
  ) +
  ylim(0, 1)


# ✅ 方法二：情感波动热力图（可以分来源+句子横向展示） ---------------------------------------------
library(ggplot2)
library(dplyr)

df$句号全局 <- ave(df$句号, df$来源, FUN = seq_along)

ggplot(df, aes(x = 句号全局, y = 来源, fill = 情感得分)) +
  geom_tile(color = "white", height = 0.5) +
  scale_fill_gradient2(low = "#2166AC", mid = "white", high = "#B2182B", midpoint = 0.5) +
  theme_minimal(base_size = 14, base_family = "STHeiti") +
  labs(title = "情感热力图（每句话）", x = "句子编号", y = "文本", fill = "情感得分")


# ✅ 方法三：提取极端情绪句子（Top 5 最正/负）并注释展示 -----------------------------------------
library(dplyr)

df_top <- df %>%
  arrange(情感得分) %>%
  slice(c(1:5, (n()-4):n())) %>%
  arrange(desc(情感得分))

print(df_top[, c("情感得分", "句子")])
write_csv(df_top, "/Users/fafaya/Desktop/宫老师_情绪极端句摘录.csv")



# 🌡️ 二、情感得分密度图（整体分布） -----------------------------------------------------
ggplot(df, aes(x = 情感得分, fill = 来源)) +
  geom_density(alpha = 0.6) +
  theme_minimal(base_size = 14, base_family = "STHeiti") +
  labs(
    title = "情感得分密度分布图",
    x = "情感得分",
    y = "密度",
    fill = "文本来源"
  ) +
  scale_fill_manual(values = c("#F46036", "#2E294E"))






# 🧊 三、情绪分类柱状图（手动分区） ------------------------------------------------------


df <- df %>%
  mutate(情绪类型 = case_when(
    情感得分 < 0.4 ~ "负面",
    情感得分 < 0.6 ~ "中性",
    TRUE ~ "正面"
  ))

ggplot(df, aes(x = 情绪类型, fill = 来源)) +
  geom_bar(position = "dodge") +
  theme_minimal(base_size = 14, base_family = "STHeiti") +
  scale_fill_manual(values = c("#7768AE", "#F9A03F")) +
  labs(
    title = "情绪类型分布柱状图",
    x = "情绪分类",
    y = "句子数",
    fill = "文本来源"
  )
