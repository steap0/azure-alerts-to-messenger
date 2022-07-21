import logging
import azure.functions as func
from os import getenv
from .sendmessage import send_slack_message, send_telegram_message
from .render import render_message

slack_token = getenv("SLACK_TOKEN", "")
slack_channel = getenv("SLACK_CHANNEL", "")
telegram_token = getenv("TELEGRAM_TOKEN", "")
telegram_chat_id = getenv("TELEGRAM_CHAT_ID", "")


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Send message triggered.')

    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse("Incorrect JSON data.", status_code=400)

    template = req.params.get("template")
    msg = render_message(template, req_body)

    logging.debug(f"Template: {template}")
    logging.debug(f"Message: {msg}")

    if slack_token and slack_channel:
        send_slack_message(slack_token, slack_channel, msg)
    else:
        logging.info("Slack not configured. Skipped.")

    if telegram_token and telegram_chat_id:
        send_telegram_message(telegram_token, telegram_chat_id, msg, 1 if template == "debug" else 0)
    else:
        logging.info("Telegram not configured. Skipped.")

    return func.HttpResponse("OK", status_code=200)
