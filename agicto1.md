# 一、如何格式化 ChatGPT 模型的输入
## 1.1如何使用 chat completion？
- ChatGPT由OpenAI gpt-4 最先进的模型提供支持 gpt-3.5-turbo 。
- 您可以使用或使用 gpt-4 OpenAI API 构建 gpt-3.5-turbo 自己的应用程序。
- 聊天模型将一系列消息作为输入，并返回 AI 编写的消息作为输出。
- 本指南通过几个示例 API 调用来说明聊天格式。

## 1.2 OpenAI聊天模型简介

“Chat completions”是OpenAI API的一个特色功能，它专为构建基于对话的问答系统而设计。

与传统的模型调用不同，该功能允许开发者提供一个对话历史，从而生成连续的回复。这使得API能够更好地理解上下文，并生成更自然的答复。

无论是为您的网站构建一个聊天助手，还是为某个特定主题创建一个问答系统，Chat completions都是一个非常有用的工具。
  
### 1.2.1   导入 openai 库
```
# if needed, install and/or upgrade to the latest version of the OpenAI Python library
%pip install --upgrade openai
```

```
# import the OpenAI Python library for calling the OpenAI API
import openai
```
### 1.2.2 聊天 API 调用示例

鉴于国内禁止调用官网的接口，为大家找到以下国内可用的稳定接口（教程在下面）

https://www.yuque.com/if/gpthub/xkk7qtluck33rmb4

### 1.2.3 API端点

您可以通过以下端点调用API：

https://api.fe8.cn/v1

  聊天 API 调用有两个必需的输入：
   - model ：要使用的模型的名称（例如、 gpt-3.5-turbo gpt-4 gpt-3.5-turbo-0613 gpt-3.5-turbo-16k-0613 ）
   - messages ：消息对象的列表，其中每个对象有两个必填字段：
       1. role ：信使的角色（ system 、 user 或 assistant ）
       2. content ：消息的内容（例如， Write me a beautiful poem ）

  让我们看一个聊天 API 调用示例，以了解聊天格式在实践中是如何工作的。

```
# Example OpenAI Python library request
MODEL = "gpt-3.5-turbo"
response = openai.ChatCompletion.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "你是一个精通Python语言的编程专家。"},
        {"role": "user", "content": "Python有什么特点？"},
    ],
    temperature=0.7,
)

response
print（response） 
print（response['choices'][0]['message']['content']）
```
以下是API返回的一个示例：
```
{
 'id': 'chatcmpl-EXAMPLE12345',
 'object': 'chat.completion',
 'created': 1677649420,
 'model': 'gpt-3.5-turbo',
 'usage': {'prompt_tokens': 56, 'completion_tokens': 31, 'total_tokens': 87},
 'choices': [
   {
    'message': {
      'role': 'assistant',
      'content': 'Python有以下几个特点：1. 简洁易读：Python的语法简洁明了，代码易读易写，使得开发者能够更快速地实现功能。2. 动态类型：Python是一种动态类型语言，变量的类型在运行时可以自动推断，无需显式声明。3. 高级数据结构：Python内置了许多高级数据结构，如列表、字典和集合，使得数据处理更加方便。4. 强大的标准库：Python拥有丰富的标准库，涵盖了各种领域的功能，如文件处理、网络通信、图形界面等。5. 大量的第三方库：Python拥有庞大的第三方库生态系统，可以通过安装第三方库来扩展Python的功能。6. 跨平台性：Python可以在多个操作系统上运行，包括Windows、Linux和Mac OS等。7. 可扩展性：Python可以通过C/C++编写扩展模块，提高性能，也可以与其他语言进行混合编程。8. 开源：Python是开源的，可以免费使用和修改，拥有活跃的开发者社区。总的来说，Python具有简洁易读、高效开发、丰富的库和跨平台等特点，使得它成为一种广泛应用于各个领域的编程语言。'},
    'finish_reason': 'stop',
    'index': 0
   }
  ]
}
```
返回值主要包括模型的ID、创建时间、模型名称以及生成的消息内容。

希望这个简介能帮助您开始使用OpenAI API构建您自己的聊天机器人！
