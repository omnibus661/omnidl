from os import close, system
import youtube_dl as yt
import sys
import datetime
import pandas as pd
from threading import Thread
from io import TextIOWrapper, BytesIO
import subprocess
import discord
import asyncio
import discord.utils
import sys
import datetime

GUILD_ID = 497540914869174283
CHANNEL_ID = 799111266420785172

TOKEN = "Nzk5MTA5ODc0Njg4MTk2NjM4.X_-zEA.FmRnwWVqT3kUVg9eMefNGFvk96c"
client = discord.Client()

async def idle():
    print("idle start")
    activity = discord.Activity(name="Idle", type=discord.ActivityType.playing)
    await client.change_presence(activity=activity)
    asyncio.sleep(10)
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(current_time)
    if str(current_time).startswith("10:0:"):
        try:
            with open("newurls","r") as u:
                urls = u.readlines()
            await dl(urls)
        except:
            pass

    else:    
        await idle()

async def dl(urls):
    activity = discord.Activity(name="Getting Uploads", type=discord.ActivityType.playing)
    await client.change_presence(activity=activity)

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
    original = sys.stdout
    sys.stdout = open('got', 'w')
    with yt.YoutubeDL(ydl_opts) as ydl:
        ydl.download(urls)
    sys.stdout = original

    outurls = []
    with open("got", "r") as nu:
        nurls = nu.readlines()
        for each in nurls:
            new = "https://youtu.be/"+ str(each)
            if new not in outurls:
                outurls.append(new)
            else:
                pass

    with open("urls", "a") as urls:
        for each in outurls:
            urls.write(each)
    await notify(outurls)

async def notify(outurls):
    amt = len(outurls)
    pstring = "Got "+ str(amt) + " new videos: "
    for each in outurls:
        pstring = pstring + "\n" + str(each)
    post_guild = discord.utils.get(client.guilds, id = GUILD_ID)
    post_channel = discord.utils.get(post_guild.channels, id = CHANNEL_ID)
    await post_channel.send(pstring)
    await idle()

@client.event
async def on_ready():  
    await idle()

client.run(TOKEN)