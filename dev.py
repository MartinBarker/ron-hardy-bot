import base64
import json
import requests
import configparser
import random
import os
import time
import subprocess
import discogs_client
import requests
import json
import OpenSSL
from twython import Twython
from base64 import b64encode
from TwitterAPI import TwitterAPI


config = configparser.ConfigParser()
config.read("config.cfg")
config.sections()

APP_KEY = config.get("twitter", "app_key")
APP_SECRET = config.get("twitter", "app_secret")
OAUTH_TOKEN = config.get("twitter", "oauth_token")
OAUTH_TOKEN_SECRET = config.get("twitter", "oauth_token_secret")
DISCOGS_TOKEN = config.get("discogs", "token")

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

def saveImage(imgUrl, filename):
    with open(filename, 'wb') as handle:
        response = requests.get(imgUrl, stream=True)

        if not response.ok:
            print(response)

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)

d = discogs_client.Client('ExampleApplication/0.1', user_token=DISCOGS_TOKEN)
results = d.list('117796')

# 15
for i in range(69, len(results.items)):
    # get item
    item = results.items[i]
    # get item id
    id = item.id
    # get release title text
    title = item.display_title
    # get release item url
    url = item.url
    print('url=',url, ', id=',id)
    # get release 
    discogsRelease = d.release(id)
    # get images
    discogsReleaseImages = discogsRelease.images
    # save all images
    imgCount = 0
    filenamesList=[]
    for imgDict in discogsReleaseImages:
        if imgCount < 4:
            imgUrl=imgDict.get('resource_url')
            print(str(imgCount) + ". " +imgUrl + ":" + imgUrl)
            # save image 
            print('saving image...')
            filename="img"+str(imgCount)+".jpg"
            saveImage(imgUrl, filename)
            print("opening image")
            imgFile = open(filename, 'rb')
            print("adding to list")
            filenamesList.append(filename)
            #twitter.upload_media(imgFile)

            imgCount += 1

    # add status text to tweet
    status = title + " \n " + url
    
    # STEP 1 - upload image
    TWEET_TEXT=status
    api = TwitterAPI(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET) #(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_TOKEN_KEY,ACCESS_TOKEN_SECRET)
    data = ""
    for x in range(0, 4):

        file = open(filenamesList[0], 'rb') 
        stream = file.read()
        data = data + stream

    r = api.request('media/upload', None, {'media': data})
    print('UPLOAD MEDIA SUCCESS' if r.status_code == 200 else 'UPLOAD MEDIA FAILURE')

    # STEP 2 - post tweet with a reference to uploaded image
    if r.status_code == 200:
        media_id = r.json()['media_id']
        r = api.request('statuses/update', {'status':TWEET_TEXT, 'media_ids':media_id})
        print('UPDATE STATUS SUCCESS' if r.status_code == 200 else 'UPDATE STATUS FAILURE')

    #print("adding image(s) to tweet")
    #media_ids = [twitter.upload_media(i).media_id_string for i in filenamesList]

    #response = twitter.upload_media(media=imgFile)
    print("adedd")

    try:
        print("tweeting with this text = ", status)
        #twitter.update_status(status=status, media_ids=[response['media_id']])
        
    except Exception as e:
        print("err: ", e)
    
    print("tweeted, now sleeping")
    time.sleep(1800)

