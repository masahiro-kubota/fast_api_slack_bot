# slack_api.py

import os
import logging

from fastapi import APIRouter, Request, Response
from slack_bolt import App
from slack_bolt.adapter.fastapi import SlackRequestHandler

from openai_fun import get_answer

router = APIRouter()

slack_app = App(
    token=os.getenv("SLACK_BOT_TOKEN"),
    signing_secret=os.getenv("SLACK_SIGNING_SECRET")
)

handler = SlackRequestHandler(app=slack_app)

@slack_app.message("hello")
def handle_message_events(message, say):
    logging.warning("Received Hello")
    say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"Hey there <@{message['user']}>!"},
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text":"Click Me"},
                    "action_id": "button_click"
                }
            }
        ],
        text=f"Hey there <@{message['user']}>!"
    )

@slack_app.event("app_mention")
def mention_handler(body, say):
    logging.warning("Mention Received")
    mention = body["event"]
    text = mention["text"]
    channel = mention["channel"]
    thread_ts = mention["ts"]
    answer = get_answer(text)
    logging.warning(answer)
    # スレッドでテキストをオウム返し
    say(text=answer, channel=channel, thread_ts=thread_ts)


@router.post("/api/http_trigger1023", name="slack events")
async def slack_events(request: Request) -> Response:
    '''Slackからの疎通用リクエストを受け取るためのエンドポイント'''
    logging.warning("Event Received")
    return await handler.handle(request)