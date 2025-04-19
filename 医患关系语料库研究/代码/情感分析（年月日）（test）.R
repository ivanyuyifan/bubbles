# 加载包
library(readxl)
library(dplyr)
library(ggplot2)
library(lubridate)

# 读取数据
data <- read_excel("/Users/fafaya/Desktop/bubbles/医患关系语料库研究/retained_Sina_Comments_with_sentiment(year-month-day).xlsx")

# 转换日期格式
data <- data %>%
  mutate(日期 = ymd(`标准化日期`))

# 分组：按天聚合平均情感得分
daily_sentiment <- data %>%
  group_by(日期) %>%
  summarise(
    平均情感 = mean(`情感得分`, na.rm = TRUE),
    评论数 = n()
  )

# 可视化
ggplot(daily_sentiment, aes(x = 日期, y = 平均情感)) +
  geom_line(color = "#2E86AB", size = 1.2) +
  geom_point(aes(size = 评论数), color = "#F18F01", alpha = 0.7) +
  geom_smooth(method = "loess", se = FALSE, color = "#E4572E", linetype = "dashed", size = 1) +
  scale_y_continuous(limits = c(0, 1)) +
  labs(
    title = "公众在微博上关于医患关系的情感趋势",
    subtitle = "情感得分越高表示态度越积极",
    x = "日期",
    y = "平均情感得分",
    caption = "数据来源：微博评论 · 分析工具：SnowNLP + ggplot2"
  ) +
  theme_minimal(base_family = "STHeiti") +
  theme(
    plot.title = element_text(size = 18, face = "bold", color = "#2E4053"),
    plot.subtitle = element_text(size = 14, color = "#566573"),
    axis.title = element_text(size = 13),
    axis.text = element_text(size = 11),
    legend.position = "none"
  )