import os
import time

from dotenv import load_dotenv
from flask import Flask, abort, request
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (ApiClient, Configuration, MessagingApi,
                                  ReplyMessageRequest, TextMessage)
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from openai import OpenAI

# basic setup
load_dotenv()

# environment variables check
if not (LINE_ACCESS_TOKEN := os.getenv("LINE_ACCESS_TOKEN")):
    raise ValueError("LINE_ACCESS_TOKEN environment variable is not set")
elif not (LINE_CHANNEL_SECRET := os.getenv("LINE_CHANNEL_SECRET")):
    raise ValueError("LINE_CHANNEL_SECRET environment variable is not set")
elif not (OPENAI_API_KEY := os.getenv("OPENAI_API_KEY")):
    raise ValueError("OPENAI_API_KEY environment variable is not set")
elif not (OPENAI_ASSISTANT_ID := os.getenv("OPENAI_ASSISTANT_ID")):
    raise ValueError("OPENAI_ASSISTANT_ID environment variable is not set")

# app setup
app = Flask(__name__)
gpt = OpenAI(api_key=OPENAI_API_KEY)
handler = WebhookHandler(LINE_CHANNEL_SECRET)
config = Configuration(access_token=LINE_ACCESS_TOKEN)


def query_gpt(message: str, gpt: OpenAI) -> str:
    """
    Query GPT-4 and return the response
    """
    # create thread
    thread = gpt.beta.threads.create(messages=[{"role": "user", "content": message}])

    # create run and wait for query to complete
    run = gpt.beta.threads.runs.create(
        thread_id=thread.id, assistant_id=OPENAI_ASSISTANT_ID
    )
    while run.status != "completed":
        run = gpt.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        app.logger.info(f"Run status: {run.status}")
        time.sleep(1)
    else:
        message_response = gpt.beta.threads.messages.list(thread_id=thread.id)
        messages = message_response.data
        latest_message = messages[0]
        return latest_message.content[0].text.value


@app.route("/", methods=["POST"])
def webhook_handler():
    """
    Handle incoming messages
    """
    # verify signature
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    # handle webhook request
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.error("Invalid signature")
        abort(400)

    return "OK"


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    """
    Handle incoming text messages and send them to custom GPT-4 model
    """
    app.logger.info("Processing incoming message")
    gpt_res = query_gpt(event.message.text, gpt=gpt)
    app.logger.info(f"GPT Response: {gpt_res}")
    with ApiClient(config) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                replyToken=event.reply_token or "",
                messages=[
                    TextMessage(
                        text=gpt_res,
                        quickReply=None,
                        quoteToken=None,
                    )
                ],
                notificationDisabled=False,
            )
        )


if __name__ == "__main__":
    app.run(
        debug=True,
        host=os.getenv("HOST") or "127.0.0.1",
        port=int(os.getenv("PORT") or 5000),
    )
