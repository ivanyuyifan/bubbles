library(readxl)
library(dplyr)
library(ggplot2)
library(showtext)    # 解决中文字体
library(tidygraph)   # 做网络图
library(ggraph)
library(RColorBrewer)

# 开启 showtext，自动为中文加载系统字体（macOS 常用 STHeiti）
showtext_auto()


# A. 词频 Top 20 横向柱状图 ------------------------------------------------------


# 1️⃣ 读取 Top100 词频表
freq_path <- "/Users/fafaya/Desktop/bubbles/医患关系语料库研究/word_frequency_top100.xlsx"
freq_df   <- read_excel(freq_path) %>% 
  arrange(desc(频数)) %>% 
  slice_head(n = 20)         # 取前 20

# 2️⃣ 绘制横向 bar
ggplot(freq_df,
       aes(x = reorder(词语, 频数), y = 频数, fill = 频数)) +
  geom_col(width = .75, show.legend = FALSE) +
  coord_flip() +
  scale_fill_gradient(low = "#6BB5FF", high = "#004C97") +
  labs(title = "医患微博语料 · 高频词 Top 20",
       x = NULL, y = "出现次数") +
  theme_minimal(base_family = "STHeiti") +
  theme(plot.title = element_text(size = 18, face = "bold", colour = "#1F4E79"),
        axis.text  = element_text(size = 12))


# B. 关键词 ↔ 共现词 网络拓扑图 ------------------------------------------------------

# 1️⃣ 读取「关键词上下文词频」数据
edge_path <- "/Users/fafaya/Desktop/bubbles/医患关系语料库研究/关键词上下文词频统计.xlsx"
edge_df   <- read_excel(edge_path)

# 2️⃣ 过滤：只保留出现 ≥3 次的共现（可自行调节阈值）
edge_df   <- edge_df %>% filter(频数 >= 3)

# 3️⃣ 构建图对象
graph <- tbl_graph(
  nodes = data.frame(name = unique(c(edge_df$关键词, edge_df$共现词))),
  edges = edge_df %>% transmute(from = 关键词, to = 共现词, weight = 频数),
  directed = FALSE
)

# 4️⃣ 绘图
set.seed(42)  # 布局可复现
ggraph(graph, layout = "fr") +   # fruchterman‑reingold 布局
  geom_edge_link(aes(width = weight),
                 colour = "#F18F01",
                 alpha  = .6) +
  geom_node_point(aes(size = centrality_degree()),
                  colour = "#2E86AB") +
  geom_node_text(aes(label = name),
                 repel = TRUE,
                 size = 3,
                 family = "STHeiti") +
  scale_edge_width(range = c(.2, 3)) +
  scale_size(range = c(3, 12)) +
  theme_void() +
  theme(legend.position = "none") +
  labs(title = "医患关键词 – 共现词 语义网络",
       subtitle = "节点大小 = 度中心性 · 边粗细 = 共现频数")

