#如何格式化 ChatGPT 模型的输入

ChatGPT由OpenAI gpt-4 最先进的模型提供支持 gpt-3.5-turbo 。
您可以使用或使用 gpt-4 OpenAI API 构建 gpt-3.5-turbo 自己的应用程序。
聊天模型将一系列消息作为输入，并返回 AI 编写的消息作为输出。
本指南通过几个示例 API 调用来说明聊天格式。

##1. 导入 openai 库
**# if needed, install and/or upgrade to the latest version of the OpenAI Python library
%pip install --upgrade openai**
**# import the OpenAI Python library for calling the OpenAI API
import openai**
##2. 聊天 API 调用示例

聊天 API 调用有两个必需的输入：
model ：要使用的模型的名称（例如、 gpt-3.5-turbo gpt-4 gpt-3.5-turbo-0613 gpt-3.5-turbo-16k-0613 ）
messages ：消息对象的列表，其中每个对象有两个必填字段：
role ：信使的角色（ system 、 user 或 assistant ）
content ：消息的内容（例如， Write me a beautiful poem ）
消息还可以包含一个可选 name 字段，该字段为信使命名。例如， ， Alice ， example-user . BlackbeardBot 名称不能包含空格。
自 2023 年 6 月起，您还可以选择提交一个列表 functions ，告知 GPT 是否可以生成 JSON 以馈送到函数中。有关详细信息，请参阅文档、API 参考或说明书指南如何使用聊天模型调用函数。
通常，对话将从告诉助理如何行为的系统消息开始，然后是交替的用户和助理消息，但你不需要遵循此格式。

让我们看一个聊天 API 调用示例，以了解聊天格式在实践中是如何工作的。

**# Example OpenAI Python library request
MODEL = "gpt-3.5-turbo"
response = openai.ChatCompletion.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Knock knock."},
        {"role": "assistant", "content": "Who's there?"},
        {"role": "user", "content": "Orange."},
    ],
    temperature=0,
)

response**

<OpenAIObject chat.completion id=chatcmpl-7UkgnSDzlevZxiy0YjZcLYdUMz5yZ at 0x118e394f0> JSON: {
  "id": "chatcmpl-7UkgnSDzlevZxiy0YjZcLYdUMz5yZ",
  "object": "chat.completion",
  "created": 1687563669,
  "model": "gpt-3.5-turbo-0301",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Orange who?"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 39,
    "completion_tokens": 3,
    "total_tokens": 42
  }
}

如您所见，响应对象有几个字段：
id ：请求的 ID
object ：返回对象的类型（例如， chat.completion ）
created ：请求的时间戳
model ：用于生成响应的模型的全名
usage ：用于生成回复、计数提示、完成和总计的令牌数
choices ：完成对象的列表（只有一个，除非您设置为 n 大于 1）
message ：模型生成的消息对象，使用 role 和 content
finish_reason ：模型停止生成文本的原因（ stop 如果达到限制， length 或者） max_tokens
index ：选项列表中的完成索引

仅提取回复：

**response['choices'][0]['message']['content']**

'Orange who?'

即使是非基于对话的任务也可以通过将指令放在第一个用户消息中来适应聊天格式。

例如，要要求模型以海盗黑胡子的风格解释异步编程，我们可以按如下方式构建对话：

**# example with a system message
response = openai.ChatCompletion.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain asynchronous programming in the style of the pirate Blackbeard."},
    ],
    temperature=0,
)

print(response['choices'][0]['message']['content'])**

**# example without a system message
response = openai.ChatCompletion.create(
    model=MODEL,
    messages=[
        {"role": "user", "content": "Explain asynchronous programming in the style of the pirate Blackbeard."},
    ],
    temperature=0,
)

print(response['choices'][0]['message']['content'])**

##3. 指导 gpt-3.5-涡轮-0301 的提示

指导模型的最佳做法可能会因模型版本而异。以下建议适用于 gpt-3.5-turbo-0301 也可能不适用于未来的模型。

###System messages 系统消息

系统消息可用于为助手准备不同的个性或行为。
请注意， gpt-3.5-turbo-0301 通常不会像 或 那样 gpt-4-0314 gpt-3.5-turbo-0613 关注系统消息。因此，对于 gpt-3.5-turbo-0301 ，我们建议改为在用户消息中放置重要说明。一些开发人员发现，在对话接近结束时不断移动系统消息，以防止模型的注意力随着对话时间的延长而转移。

**# An example of a system message that primes the assistant to explain concepts in great depth
response = openai.ChatCompletion.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "You are a friendly and helpful teaching assistant. You explain concepts in great depth using simple terms, and you give examples to help people learn. At the end of each explanation, you ask a question to check for understanding"},
        {"role": "user", "content": "Can you explain how fractions work?"},
    ],
    temperature=0,
)

print(response["choices"][0]["message"]["content"])**

###Few-shot prompting 少数镜头提示
在某些情况下，向模型展示您想要的内容比告诉模型您想要什么更容易。
向模型显示所需内容的一种方法是使用伪造的示例消息。

例如：
**# An example of a faked few-shot conversation to prime the model into translating business jargon to simpler speech
response = openai.ChatCompletion.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "You are a helpful, pattern-following assistant."},
        {"role": "user", "content": "Help me translate the following corporate jargon into plain English."},
        {"role": "assistant", "content": "Sure, I'd be happy to!"},
        {"role": "user", "content": "New synergies will help drive top-line growth."},
        {"role": "assistant", "content": "Things working well together will increase revenue."},
        {"role": "user", "content": "Let's circle back when we have more bandwidth to touch base on opportunities for increased leverage."},
        {"role": "assistant", "content": "Let's talk later when we're less busy about how to do better."},
        {"role": "user", "content": "This late pivot means we don't have time to boil the ocean for the client deliverable."},
    ],
    temperature=0,
)

print(response["choices"][0]["message"]["content"])**

为了帮助阐明示例消息不是实际对话的一部分，并且不应由模型引用，您可以尝试将消息 name 字段 system 设置为 example_user 和 example_assistant 。

转换上面的几个镜头示例，我们可以这样写：

**# The business jargon translation example, but with example names for the example messages
response = openai.ChatCompletion.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "You are a helpful, pattern-following assistant that translates corporate jargon into plain English."},
        {"role": "system", "name":"example_user", "content": "New synergies will help drive top-line growth."},
        {"role": "system", "name": "example_assistant", "content": "Things working well together will increase revenue."},
        {"role": "system", "name":"example_user", "content": "Let's circle back when we have more bandwidth to touch base on opportunities for increased leverage."},
        {"role": "system", "name": "example_assistant", "content": "Let's talk later when we're less busy about how to do better."},
        {"role": "user", "content": "This late pivot means we don't have time to boil the ocean for the client deliverable."},
    ],
    temperature=0,
)

print(response["choices"][0]["message"]["content"])**

并非每次工程对话的尝试一开始都会成功。
如果你的第一次尝试失败了，不要害怕尝试不同的方法来启动或调节模型。
例如，一位开发人员发现，当他们插入一条用户消息时，准确性有所提高，该消息说“到目前为止做得好，这些已经很完美”，以帮助模型提供更高质量的响应。
有关如何提高模型可靠性的更多想法，请考虑阅读我们关于提高可靠性的技术指南。它是为非聊天模型编写的，但它的许多原则仍然适用。

###4. 计算代币

提交请求时，API 会将消息转换为一系列令牌。

使用的令牌数量会影响：
1. 使用的令牌数量会影响：
2. 生成响应所需的时间
3. 当回复被切断达到最大令牌限制（4，096 for 或 8，192 for gpt-3.5-turbo gpt-4 ）
   
您可以使用以下函数来计算消息列表将使用的令牌数。
请注意，从消息中计算令牌的确切方式可能会因模型而异。考虑以下函数的计数，而不是永恒的保证。
特别是，使用可选函数输入的请求将在下面计算的估计值之上消耗额外的令牌。

**import tiktoken


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
        tokens_per_name = -1  # if there's a name, the role is omitted
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
    return num_tokens**

    **# let's verify the function above matches the OpenAI API response

import openai

example_messages = [
    {
        "role": "system",
        "content": "You are a helpful, pattern-following assistant that translates corporate jargon into plain English.",
    },
    {
        "role": "system",
        "name": "example_user",
        "content": "New synergies will help drive top-line growth.",
    },
    {
        "role": "system",
        "name": "example_assistant",
        "content": "Things working well together will increase revenue.",
    },
    {
        "role": "system",
        "name": "example_user",
        "content": "Let's circle back when we have more bandwidth to touch base on opportunities for increased leverage.",
    },
    {
        "role": "system",
        "name": "example_assistant",
        "content": "Let's talk later when we're less busy about how to do better.",
    },
    {
        "role": "user",
        "content": "This late pivot means we don't have time to boil the ocean for the client deliverable.",
    },
]

for model in [
    "gpt-3.5-turbo-0301",
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
    print()**
