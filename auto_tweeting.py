import socket
import time
from os import path
import requests
import tweepy
import urllib3
from bs4 import BeautifulSoup as Bs

printed = False

lis = 1

common_phrases = [None, 'YouTube','YouTube Home', 'Upload', 'Home', 'Trending', 'History', 'Get YouTube Premium', 'Music',
                  'Sports', 'Gaming', 'Movies', 'News', 'Live', 'Fashion', 'Spotlight', '360° Video', 'Browse channels',
                  'Website', 'Facebook', 'Twitter', 'Instagram', '"Bae" Out Now!', 'YouTube home', 'Instargram',
                  'Malang Title Track : LIVE NOW', 'Blogger', 'TV Shows', 'Get YouTube TV']

# channel url
base_url = "https://www.youtube.com/channel/"
channel_id = ""
url = base_url + channel_id + "/videos"

# twitter api
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""
y_api = ""


def connect_to_twitter():
    try:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        # Create API object
        ap = tweepy.API(auth)
    except (urllib3.exceptions.MaxRetryError, urllib3.exceptions.NewConnectionError, socket.gaierror,
            requests.exceptions.ConnectionError):
        time.sleep(15)
        return connect_to_twitter()
    else:
        print('Twitter connected')
        return ap


def connect_to_youtube():
    global printed, url
    try:
        respons = requests.get(url)
    except (urllib3.exceptions.MaxRetryError, urllib3.exceptions.NewConnectionError, socket.gaierror,
            requests.exceptions.ConnectionError):
        print('Retrying connection in 15 secs')
        time.sleep(15)
        return connect_to_youtube()
    else:
        if not printed:
            print('Channel connected(secured connection)')
            printed = True
        return respons


def form_vid_link():
    global vlink
    vi_link = vlink[lis]
    vi_link = vi_link.replace("watch?v=", "")
    vi_link = "https://youtu.be" + vi_link
    return vi_link


def tweet_text(msg):
    try:
        api.update_status(msg)
    except tweepy.error.TweepError:
        print("Video already posted")
    else:
        print('Posting new video')


def ids_vlinks():
    global soup
    for link in soup.find_all("a"):
        ids.append(link.get("title"))
        vlink.append(link.get("href"))

    for phrase in common_phrases:
        for x in range(ids.count(phrase)):
            vlink.pop(ids.index(phrase))
            ids.remove(phrase)


"""
def print_elapsed_time():
    global ini_time
    final_time = time.time()
    elapsed_time = final_time - ini_time
    if elapsed_time <= 60:
        print(f'Time = {int(elapsed_time)} secs')
    elif 60 < elapsed_time <= 3600:
        mins = elapsed_time // 60
        secs = elapsed_time - (60 * mins)
        print(f'Time = {int(mins)} mins {int(secs)} secs')
    elif elapsed_time > 3600:
        hours = elapsed_time // 3600
        new_tm = elapsed_time - (hours * 3600)
        if new_tm <= 60:
            print(f"Time = {int(hours)} hrs {int(new_tm)} secs")
        elif new_tm > 60:
            mins = new_tm // 60
            secs = new_tm - (mins * 60)
            print(f'Time = {int(hours)} hrs {int(mins)} mins {int(secs)} secs')
"""

api = connect_to_twitter()
# connect to channel
response = connect_to_youtube()
soup = Bs(response.text, "html.parser")

# list of videos
ids = []
vlink = []

ids_vlinks()
print(ids)
prev_video = ''

if not path.exists('data/video.txt'):
    file = open('data/video.txt', 'x')
    print('File created named "video.txt"')
    prev_video = ids[1]
    file.close()
    file = open('data/video.txt', 'w')
    try:
        file.write(prev_video)
    except UnicodeEncodeError:
        pass
    file.close()
elif path.exists('data/video.txt'):
    file = open('data/video.txt', 'r')
    try:
        prev_video = file.read()
    except UnicodeDecodeError:
        prev_video = ''
    file.close()
if prev_video == '':
    prev_video = ""
ids.clear()
vlink.clear()

response.close()
print('Previous Video:- ' + prev_video)

while True:
    brake = False
    response = connect_to_youtube()
    soup = Bs(response.text, "html.parser")

    ids_vlinks()

    new_vid_name = ids[lis]
    if new_vid_name == prev_video:
        print("Latest Video:- " + new_vid_name)
    if new_vid_name != prev_video:
        prev_video = new_vid_name
        file = open('data/video.txt', 'w')
        try:
            file.write(prev_video)
        except UnicodeEncodeError:
            pass
        file.close()

        print("New Video:- " + new_vid_name)

        new_vid_link = form_vid_link()

        status = new_vid_name + '\n' * 2

        status += '\n' + new_vid_link

        tweet_text(status)
    response.close()
    ids.clear()
    vlink.clear()
    break
