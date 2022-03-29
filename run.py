import logging
import pprint
import schedule
from get_ctfinfo import get_ctfinfo
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime, date, timedelta
import time
import re
from threading import Thread, Lock


env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

logging.basicConfig(level=logging.DEBUG)
app = App(token=os.environ['SLACK_TOKEN'])
announce_channel = "general"

ctf_infos = get_ctfinfo()
lock = Lock()


def week_do():
    global ctf_infos
    lock.acquire()
    print("aaa")
    ctf_infos = get_ctfinfo()

    for one in ctf_infos:
        app.client.chat_postMessage(
            channel=announce_channel,
            blocks=one["text"]
        )

    lock.release()


@app.action("button-click")
def apply_event(body, ack, say):
    ack()
    lock.acquire()
    for one in ctf_infos:
        if one["ctftime-url"] == body["actions"][0]['value']:
            lower_title = one["title"].lower()
            channel_name = re.sub("[^a-zA-Z0-9]+", "_", lower_title)
            channel_id = None
            for chan in app.client.conversations_list(limit=1000)["channels"]:
                if channel_name == chan["name"]:
                    channel_id = chan["id"]
                    break
            one["text"].pop(4)
            if channel_id is None:
                response = app.client.conversations_create(name=channel_name)
                channel_id = response["channel"]["id"]
                app.client.chat_postMessage(channel=channel_name, blocks=one["text"])
            channel_link = \
                {
                    "text": {
                        "type": "mrkdwn",
                        "text": f"<#{channel_id}|{channel_name}>"
                    },
                    "type": "section"
                }
            one["text"].insert(-1, channel_link)
            mes_ts = body["container"]["message_ts"]
            app.client.chat_update(channel=body["channel"]["id"], ts=mes_ts, blocks=one["text"])
            break

    lock.release()


def run_loop():
    schedule.every().thursday.at("03:00").do(week_do)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    t1 = Thread(target=run_loop)
    t1.start()
    week_do()
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
