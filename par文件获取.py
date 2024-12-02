#使用前请先激活CoreNLP 服务器地址，详细请参考notion
import requests

# 设置 CoreNLP 服务器地址
CORENLP_SERVER_URL = "http://localhost:9000"

# 输入和输出文件路径
input_file = "/Users/fafaya/Desktop/bubbles/测试文字.txt"   # 你的 .txt 文件
output_file = "/Users/fafaya/Desktop/bubbles/测试文字output.par" # 保存解析结果的文件

# 读取输入文件内容
with open(input_file, "r", encoding="utf-8") as f:
    text = f.read()

# 设置解析参数
params = {
    "annotators": "tokenize,ssplit,pos,lemma,parse,depparse",  # 分词、句法树、依存解析
    "outputFormat": "json"                                    # 返回 JSON 格式
}

# 向服务器发送请求
response = requests.post(
    f"{CORENLP_SERVER_URL}/?properties={str(params)}",
    data=text.encode('utf-8')
)

# 检查返回结果并保存到文件
if response.ok:
    parsed_data = response.json()
    with open(output_file, "w", encoding="utf-8") as f:
        for sentence in parsed_data["sentences"]:
            # 写入短语结构树
            f.write(f"Parse Tree:\n{sentence['parse']}\n")
            # 写入依存关系
            f.write("Dependencies:\n")
            for dep in sentence["basicDependencies"]:
                f.write(f"{dep['dep']}({dep['governorGloss']}, {dep['dependentGloss']})\n")
            f.write("\n")
    print(f"解析完成，结果已保存到 {output_file}")
else:
    print("解析失败:", response.text)
