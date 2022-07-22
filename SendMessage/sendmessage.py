import logging
import requests
from time import sleep


def send_message(method: str, url: str, headers: dict = {}, json: dict = {}, retry_limit: int = 5) -> str:
    try:
        if method == "POST":
            r = requests.post(url=url, headers=headers, json=json)
        elif method == "GET":
            r = requests.get(url=url, headers=headers, json=json)
        else:
            logging.error(f"Wrong method: {method}")
            return {}
    except requests.exceptions.ConnectionError as e:
        logging.error(f"Connection error: {e}")
        if retry_limit > 0:
            logging.error("Connection retry.")
            sleep(10)
            send_message(method, url, headers, json, retry_limit-1)
        else:
            logging.error("Can't send message!")
            return {}

    if r.status_code != 200:
        logging.error(f"Wrong status code: {r.status_code}")
        if retry_limit > 0:
            logging.error("Connection retry.")
            sleep(5)
            send_message(method, url, headers, json, retry_limit-1)
        else:
            return {}

    try:
        if r.json():
            return r.json()
        else:
            return {}
    except KeyError:
        return {}


def send_slack_message(token: str, channel: str, text: str) -> None:
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    json = {
        "channel": channel,
        "text": text
    }

    result = send_message("POST", url, headers, json)

    if result:
        if result["ok"]:
            logging.info(f'Message sent to Slack channel {result["channel"]}.')
            return
        else:
            logging.error(f"Message sending error: {result}")
            return
    else:
        logging.error(f"Message sending error: {result}")
        return


def send_telegram_message(token: str, chat_id: str, text: str, debug: bool = 0) -> None:
    if debug:
        url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={text}"
    else:
        url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&parse_mode=markdown&text={text}"

    result = send_message("GET", url)

    if result:
        if result["ok"]:
            logging.info(
                f'Message sent to Telegram chat {result["result"]["chat"]["id"]}.')
            return
        else:
            logging.error(f"Message sending error: {result}")
            return
    else:
        logging.error(f"Message sending error: {result}")
        return
