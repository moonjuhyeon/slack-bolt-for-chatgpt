import os
import asyncio
from threading import Timer
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler
from slack_bolt.app.async_app import AsyncApp

import ChatGPT


# Initializes your app with your bot token and socket mode handler
app = AsyncApp(token=os.environ["SLACK_BOT_TOKEN"])
THREAD_TIMEOUT_SECONDS = 300

# 스레드의 thread_ts 값을 저장하기 위한 딕셔너리
threads = {}


async def remove_thread(ts):
    if ts in threads:
        del threads[ts]


@app.event("app_mention")
async def handle_mention(event, say):
    # 새로운 스레드를 시작합니다.
    user_id = event["user"]
    response = f"<@{user_id}>님 안녕하세요 무엇을 도와드릴까요?"
    result = await say(text=response)
    # 이 스레드의 ts 값을 저장합니다.
    thread_ts = result["ts"]
    threads[thread_ts] = {"channel": event["channel"], "messages": [], "isBot": True}
    # 대화 스레드를 삭제하기 위한 타이머를 시작합니다.
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, Timer, THREAD_TIMEOUT_SECONDS, remove_thread, [thread_ts])


@app.event("message")
async def handle_message(event, say):
    # 메시지를 작성한 유저가 bot인 경우 무시합니다.
    if "bot_id" in event:
        return
    # 이전에 시작된 스레드에 대한 정보를 가져옵니다.
    thread_ts = event.get("thread_ts")
    if thread_ts is None:
        thread_ts = threads.get(event["ts"])
    if thread_ts is None:
        return

    # 이전에 시작된 스레드가 삭제된 경우 처리합니다.
    if thread_ts not in threads:
        return

    # 이전에 시작된 스레드에 대한 응답 메시지를 작성합니다.
    message = event["text"]
    threads[thread_ts]["messages"].append({"role": "user", "content": message})
    response = ChatGPT.ChatGPT(threads[thread_ts]["messages"])
    # 이전에 시작된 스레드에 응답 메시지를 전송합니다.
    await say(text=response, channel=threads[thread_ts]["channel"], thread_ts=thread_ts)
    # 대화 스레드에 대화 내용을 추가합니다.
    threads[thread_ts]["messages"].append({"role": "assistant", "content": response})

    # 대화 스레드를 삭제하기 위한 타이머를 시작합니다.
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, Timer, THREAD_TIMEOUT_SECONDS, remove_thread, [thread_ts])


async def main():
    handler = AsyncSocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    await handler.start_async()

# Start your app
if __name__ == "__main__":
    asyncio.run(main())
