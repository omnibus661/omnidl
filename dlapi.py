import json
import sys
import os
import logging
import asyncio
from threading import Thread
from time import sleep
from flask import Flask, abort, request, Response, send_from_directory
from flask_restful import Resource, Api
from flask_jsonpify import jsonify
from flask_cors import CORS
import youtube_dl as yt
import sys
import glob
import shutil

USERS = [
    "omni",
    "omnibus"
]

HOST = "omnijunk.xyz"
PORT = 66
MAINDIR = "/scripts/ytapi"
# flask base
app = Flask(__name__)
api = Api(app)
CORS(app)

def ytdl(vid):
    urls = []
    ydl_opts = {
        'format': 'mp4',
    }
    if "https://youtu.be/" in vid:
        urls.append(vid)
    elif "https://youtube.com/" in vid:
        modid = vid.replace("https://www.youtube.com/watch?v=","")
        modid = "https://youtu.be/" + str(vid)
        urls.append(modid)
    else:
        modid = "https://youtu.be/" + str(vid)
        urls.append(modid)

    with yt.YoutubeDL(ydl_opts) as ydl:
        ydl.download(urls)
    print("done downloading.")
    sleep(1)

class base(Resource):
    def post(self):
        return {"RESPONSE":405}

    def get(self):
        vid = request.args['id']
        user = request.args['u']
        conf = request.args['dl']
        if vid != "" or user != "":
            if user in USERS:
                #print(str(vid))
                thread = Thread(target = ytdl, args = (vid, ))
                thread.start()
                thread.join()

                globstr = "*"+ str(vid)+".mp4"
                files = glob.glob(str(globstr))
                print(files)
                filename = files[0]

                if conf == "y":
                    return send_from_directory(MAINDIR,filename, as_attachment = True)
                else:
                    return {"RESPONSE":200}
            else:
                return {"RESPONSE":401}
        else:
            return {"RESPONSE":400}




if __name__ == '__main__':
    import logging
    logging.basicConfig(filename='DB_Server.log',level=logging.ERROR)
        
    if sys.platform == "linux":
        os.system('clear')
    elif sys.platform == "win32":
        os.system('cls')
    else:
        print("Now running on port "+str(PORT))

    api.add_resource(base,'/') # send raw request data to database
    #api.add_resource(view,'/dl')
    #api.add_resource(QueryDB,'/query/')
    app.run(host=HOST,port=PORT,debug=False)

 