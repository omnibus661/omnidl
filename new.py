from os import close
import youtube_dl as yt
import sys
import datetime
import pandas as pd
from threading import Thread
from io import TextIOWrapper, BytesIO
import subprocess

import time
try:
    with open("newurls","r") as u:
    
        urls = u.readlines()
except:
    sys.exit()



def dl(urls):
    sys.stdout = open('got', 'w')
    with yt.YoutubeDL(ydl_opts) as ydl:
        ydl.download(urls)
    sys.stdout.close()


today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
daterange = pd.date_range(start=yesterday,end=today)


ydl_opts = {
    "simulate": True,
    "forceid": True,
    "daterange": daterange,
    "ignoreerrors": True,
    "skip_download": True,
    "quiet": True
}
outurls = []

thread = Thread(target = dl, args = (urls, ))
thread.start()
thread.join()


with open("got", "r") as nu:
    nurls = nu.readlines()
    for each in nurls:
        new = "https://youtu.be"+ str(each)
        outurls.append(new)

print(outurls)


