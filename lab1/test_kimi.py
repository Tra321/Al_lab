from openai import OpenAI
import sys

# 初始化客户端
client = OpenAI(
    api_key = "sk-LbrfATC7g6FH50AR3VpXxMS3y2wBFWeezLWsg0KnBePZVFHa", # 请替换为你自己复制的Key
    base_url = "https://api.moonshot.cn/v1" # Kimi的API地址
)

# 调用API进行对话
completion = client.chat.completions.create(
    model = "kimi-k2.5", # 指定模型, kimi-k2.5是当前最新模型
    messages = [
        {"role": "system", "content": "你是一个乐于助人的助手。"},
        {"role": "user", "content": "请简单介绍一下你自己。"}
    ]
)
# 打印回复
print(completion.choices[0].message.content)
