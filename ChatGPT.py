import os
import openai

# 발급받은 OpenAI API Key 기입
API_KEY = os.environ.get("CHAT_GPT_TOKEN")


def ChatGPT(messages):
    # api key 세팅
    openai.api_key = API_KEY

    # ChatGPT API 호출하기
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo-0301',
        messages=messages
    )

    return response['choices'][0]['message']['content']
