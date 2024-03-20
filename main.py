from flask import abort, request
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (ApiClient, MessagingApi, ReplyMessageRequest,
                                  TextMessage)
from linebot.v3.webhooks import MessageEvent, TextMessageContent

from config import FirestoreConfig, GPTChatBotConfig, LineConfig, OpenAiConfig
from gpt_chatbot import GPTChatbot

# basic setup
config = GPTChatBotConfig(
    line=LineConfig(),
    openai=OpenAiConfig(),
    firestore=FirestoreConfig(),
)
app = GPTChatbot(config)


# flask routes
@app.server.route("/", methods=["POST"])
def webhook_handler():
    """
    Handle incoming messages
    """
    # verify signature
    signature = request.headers.get("X-Line-Signature")
    if not signature:
        return "Signature not found", 400

    body = request.get_data(as_text=True)

    # handle webhook request
    try:
        app.chatbot.handler.handle(body, signature)
    except InvalidSignatureError:
        app.server.logger.error("Invalid signature")
        abort(400)

    return "OK"


# line handler
@app.chatbot.handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    """
    Handle incoming text messages and send them to custom GPT-4 model
    """
    try:
        # get the message from GPT
        app.server.logger.info("Processing incoming message")
        gpt_res = app.send_gpt_query(event)
        app.server.logger.info(f"GPT Response: {gpt_res}")

        # send the response back to the user
        with ApiClient(app.chatbot.config) as api_client:
            line_bot_api = MessagingApi(api_client)
            res = line_bot_api.reply_message_with_http_info(
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

            # get sent message id
            if isinstance(line_res := res.raw_data, str):
                app.store_gpt_response(event, line_res, gpt_res)

    except Exception as err:
        app.server.logger.error("Error processing message", err)


def create_app():
    app.server.logger.info("Creating app")
    return app.server
