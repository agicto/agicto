import tiktoken
import os
import openai

# 加载 .env 到环境变量
from dotenv import load_dotenv, find_dotenv
 
_ = load_dotenv(find_dotenv())

# print(find_dotenv())
# 配置 OpenAI 服务
openai.api_key = os.getenv("OPENAI_API_KEY")  # 设置 OpenAI 的 key
openai.api_base = os.getenv("OPENAI_API_BASE")  # 指定代理地址


def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613"):
    """Return the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model in {
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k-0613",
        "gpt-4-0314",
        "gpt-4-32k-0314",
        "gpt-4-0613",
        "gpt-4-32k-0613",
        }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # 如果有名称，则省略角色
    elif "gpt-3.5-turbo" in model:
        print("Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613.")
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613")
    elif "gpt-4" in model:
        print("Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.")
        return num_tokens_from_messages(messages, model="gpt-4-0613")
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
        )
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens

# 让我们验证上面的函数与OpenAI API响应是否匹配

import openai

example_messages = [
    {
        "role": "system",
        "content": "你是一个乐于助人、循规蹈矩的助手，能把公司的行话翻译成通俗易懂的英语。",
    },
    {
        "role": "system",
        "name": "example_user",
        "content": "新的协同效应将有助于推动营收增长。",
    },
    {
        "role": "system",
        "name": "example_assistant",
        "content": "如果一切都运转良好，就会增加收入。",
    },
    {
        "role": "system",
        "name": "example_user",
        "content": "当我们有更多的带宽可以接触到增加杠杆的机会时，让我们回过头来。",
    },
    {
        "role": "system",
        "name": "example_assistant",
        "content": "等我们不那么忙的时候再谈如何做得更好。",
    },
    {
        "role": "user",
        "content": "这个迟来的支点意味着我们没有时间为客户交付的成果翻云覆雨。",
    },
]

for model in [
    "gpt-3.5-turbo-0613",
    "gpt-3.5-turbo",
    "gpt-4-0314",
    "gpt-4-0613",
    "gpt-4",
    ]:
    print(model)
    # example token count from the function defined above
    print(f"{num_tokens_from_messages(example_messages, model)} prompt tokens counted by num_tokens_from_messages().")
    # example token count from the OpenAI API
    response = openai.ChatCompletion.create(
        model=model,
        messages=example_messages,
        temperature=0,
        max_tokens=1,  # we're only counting input tokens here, so let's not waste tokens on the output
    )
    print(f'{response["usage"]["prompt_tokens"]} prompt tokens counted by the OpenAI API.')
    print()
