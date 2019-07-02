# also need to install win32api
from win10toast import ToastNotifier # pip install win10toast
import urllib.request
import json

# One-time initialization
toaster = ToastNotifier()

API_KEY = "AIzaSyD4a5qZCNfXIq7j0EcOB6pbonCY7eeEyFg"
CHANNEL_ID = 'UCeVmancWx92vTZ9IPYOKnKg'
old_subs = 0
while True:
    
    data = urllib.request.urlopen("https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&id={}&key={}".format(CHANNEL_ID,API_KEY)).read()
    name = json.loads(data)["items"][0]["snippet"]["title"]
    new_subs = json.loads(data)["items"][0]["statistics"]["subscriberCount"]
    view_count = json.loads(data)["items"][0]["statistics"]["viewCount"]
    comment_count = json.loads(data)["items"][0]["statistics"]["commentCount"]
    
    if int(new_subs) > int(old_subs):
        toaster.show_toast("You Got New Subscriber!!!!",
                       name + " has " + "{:,d}".format(int(new_subs)) + " subscribers!",
                       icon_path=None,
                       duration=10)

        while toaster.notification_active():
            time.sleep(0.1)

    if int(new_subs) < int(old_subs):
        diff = old_subs - int(new_subs)
        toaster.show_toast("You Lose {} Subscriber ".format(diff),
                       name + " has " + "{:,d}".format(int(new_subs)) + " subscribers!",
                       icon_path=None,
                       duration=10)

        while toaster.notification_active():
            time.sleep(0.1)

    old_subs = int(new_subs)
