import requests
import json
import os

API_KEY = os.getenv("YOUTUBE_API_KEY")
CHANNEL_ID = os.getenv("CHANNEL_ID")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

STATE_FILE = "state.json"


def load_state():
    if not os.path.exists(STATE_FILE):
        return {"is_live": False}
    with open(STATE_FILE, "r") as f:
        return json.load(f)


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": message
    })


def get_live_video():
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "channelId": CHANNEL_ID,
        "eventType": "live",
        "type": "video",
        "key": API_KEY
    }

    response = requests.get(url, params=params).json()
    items = response.get("items", [])

    if items:
        video_id = items[0]["id"]["videoId"]
        title = items[0]["snippet"]["title"]
        return video_id, title

    return None, None


import requests
import json
import os
from datetime import datetime

API_KEY = os.getenv("YOUTUBE_API_KEY")
CHANNEL_ID = os.getenv("CHANNEL_ID")
TG_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

STATE_FILE = "state.json"


def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})


def get_state():
    if not os.path.exists(STATE_FILE):
        return {"live": False, "videoId": None}

    with open(STATE_FILE, "r") as f:
        return json.load(f)


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


def get_live_video():
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "channelId": CHANNEL_ID,
        "eventType": "live",
        "type": "video",
        "key": API_KEY
    }

    res = requests.get(url, params=params).json()
    items = res.get("items", [])

    if not items:
        return None, None

    vid = items[0]["id"]["videoId"]
    title = items[0]["snippet"]["title"]
    return vid, title


def main():
    state = get_state()
    video_id, title = get_live_video()
    is_live = video_id is not None

    # STATE CHANGE LOGIC (IMPORTANT)
    if is_live and not state["live"]:
        send_telegram(f"🔴 LIVE STARTED\n{title}\nhttps://youtu.be/{video_id}")

    if not is_live and state["live"]:
        send_telegram("⚫ Stream ENDED")

    # Save state always
    save_state({
        "live": is_live,
        "videoId": video_id,
        "time": str(datetime.utcnow())
    })


if __name__ == "__main__":
    main()
