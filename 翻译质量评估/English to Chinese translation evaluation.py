from gensim.models.fasttext import load_facebook_vectors
import numpy as np
from torch import cosine_similarity
import torch

# 加载fastText词向量（从fastText下载的.bin文件）
model_en = load_facebook_vectors('/Users/fafaya/Desktop/bubbles/翻译质量评估/cc.en.300.bin')
model_zh = load_facebook_vectors('/Users/fafaya/Desktop/bubbles/翻译质量评估/cc.zh.300.bin')

# 句子转换为嵌入
def get_sentence_embedding(sentence, model):
    words = sentence.split()
    word_vectors = [model[word] for word in words if word in model]
    return np.mean(word_vectors, axis=0) if word_vectors else np.zeros(300)

english_sentence = "...and now, as I sat looking at the white bed and overshadowed walls occasionally also turning a fascinated eye towards the dimly gleaning mirror..."
chinese_translations = ["接着，我坐在那儿眼望着白色的床和昏暗的四壁，偶尔还不由自主地转眼去望一望隐隐发亮的镜子...", "这时候，我坐在那儿，眼望着白色的大床和昏暗的四壁——偶尔还不由自主地转眼朝 那面隐隐发亮的镜子看上一眼...", "此刻，我坐着，一面打量着白白的床和影影绰绰的墙，不时还用经不住诱惑的目光瞟一眼泛着微光的镜子..."]

# 计算相似度
english_embedding = get_sentence_embedding(english_sentence, model_en)
english_embedding = torch.tensor(english_embedding)  # 转换为 Tensor

for idx, translation in enumerate(chinese_translations):
    chinese_embedding = get_sentence_embedding(translation, model_zh)
    chinese_embedding = torch.tensor(chinese_embedding)  # 转换为 Tensor
    similarity = torch.cosine_similarity(english_embedding.unsqueeze(0), chinese_embedding.unsqueeze(0))
    print(f"Translation {idx + 1} similarity: {similarity.item():.4f}")
