import os
import openai

# 加载 .env 到环境变量
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

# print(find_dotenv())
# 配置 OpenAI 服务
openai.api_key = os.getenv("OPENAI_API_KEY")  # 设置 OpenAI 的 key
openai.api_base = os.getenv("OPENAI_API_BASE")  # 指定代理地址

#使用Python和OpenAI API，一个最基础的互动例子如下：

response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "user", "content": "解释一下，什么是大型语言模型？"}
  ]
)
print(response.choices[0].message['content'])

#例如，如果我们希望得到一个更加专业或深入的解答，可以像下面这样设置一个专家环境：
response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "你现在是一名大型语言模型的专家"},
    {"role": "user", "content": "解释一下，什么是大型语言模型？"}
  ]
)
print(response.choices[0].message['content'])

# 错误示例
response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "user", "content": "解释一下，什么是大型语言模型？"},
    {"role": "system", "content": "你现在是一名大型语言模型的专家"}
  ]
)
