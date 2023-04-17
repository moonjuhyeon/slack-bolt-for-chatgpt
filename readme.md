# ChatGPT Slack-Bolt Bot

Slack-Bolt로 만들어진 ChatGPT Bot입니다.

### docker build
```shell
$ docker build -t slack-bolt-gpt-001 .
```

### docker run
```shell
$ docker run -d \
-e SLACK_APP_TOKEN=<SLACK_APP_TOKEN> \
-e SLACK_BOT_TOKEN=<SLACK_BOT_TOKEN> \
-e CHAT_GPT_TOKEN=<CHAT_GPT_TOKEN> \
--name slack-bolt-gpt \ 
slack-bolt-gpt-001
```