import time
import pprint
import locale
from datetime import datetime, date, timedelta
import requests

def get_day(form):
    d = datetime.strptime(f"{form['year']}-{form['month']}-{form['day']}-{form['hour']}-{form['minute']}",
                      "%Y-%m-%d-%H-%M")
    return d.strftime("%a")

def convert_post_format(title, url, start, finish, ctftime_url, weight, format1):
    block = [
        {
            "type": "divider"
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*<{url}|{title}>*"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*期間*\n{start['month']}/{start['day']}({get_day(start)}) {start['hour']}:{start['minute']} ～ {finish['month']}/{finish['day']}({get_day(finish)}) {finish['hour']}:{finish['minute']}"
            }
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": f"*ctftime:*\n<{ctftime_url}|Link>"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*weight:*\n{weight}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*format:*\n{format1}"
                },
            ]
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Join"
                    },
                    "style": "primary",
                    "value": ctftime_url,
                    "action_id": "button-click"
                }
            ]
        },
        {
            "type": "divider"
        }
    ]
    return block


def convert_JSTtime(tdata):
    s = tdata.split("T")
    t = s[1].split("+")[0].split(":")
    hour = int(t[0])
    minute = int(t[1])
    hour = hour + 9
    if hour >= 24:
        hour = hour % 24
        day = datetime.strptime(s[0], "%Y-%m-%d")
        tomorrow = day + timedelta(days=1)
        s[0] = datetime.strftime(tomorrow, "%Y-%m-%d")

    d = s[0].split("-")
    hour = str(hour).zfill(2)
    minute = str(minute).zfill(2)
    return {"year": int(d[0]), "month": int(d[1]), "day": int(d[2]), "hour": hour, "minute": minute}


def get_ctfinfo():
    curtime = int(time.time())
    now = datetime.fromtimestamp(curtime) - timedelta(hours=9)
    print("now: ", now)
    end = (now + timedelta(days=7))
    print("finish: ", end)
    end = end.timestamp()
    curtime = now.timestamp()

    payload = {"limit": 6, "start": curtime, "finish": end}
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    ret = requests.get("https://ctftime.org/api/v1/events/", params=payload, headers=headers).json()

    infos = []

    for r in ret:
        title = r["title"]
        weight = r["weight"]
        ctftime_url = r["ctftime_url"]
        url = r["url"]
        format1 = r["format"]
        start = r["start"]
        finish = r["finish"]

        if datetime.strptime(start.split("T")[0], "%Y-%m-%d").timestamp() > end:
            continue

        start = convert_JSTtime(start)
        finish = convert_JSTtime(finish)
        start_timestamp = datetime.strptime(f"{start['year']}-{start['month']}-{start['day']}-{start['hour']}-{start['minute']}", "%Y-%m-%d-%H-%M").timestamp()
        finish_timestamp = datetime.strptime(f"{finish['year']}-{finish['month']}-{finish['day']}-{finish['hour']}-{finish['minute']}", "%Y-%m-%d-%H-%M").timestamp()
        text = f"""{title}
        期間(JST)：{start['month']}/{start['day']} {start['hour']}:{start['minute']} ～ {finish['month']}/{finish['day']} {finish['hour']}:{finish['minute']}
        リンク：{url}
        形式：{format1}
        weight：{weight}
        """
        print(text)
        infos.append({"text": convert_post_format(title, url, start, finish, ctftime_url, weight, format1), "start": start_timestamp, "finish": finish_timestamp, "ctftime-url": ctftime_url, "title": title})

    return infos


if __name__ == "__main__":
    get_ctfinfo()
