import base64
import json
import requests
import configparser
import random
import os
import time
import subprocess
import discogs_client

import OpenSSL
from twython import Twython
from base64 import b64encode


config = configparser.ConfigParser()
config.read("config.cfg")
config.sections()

APP_KEY = config.get("twitter", "app_key")
APP_SECRET = config.get("twitter", "app_secret")
OAUTH_TOKEN = config.get("twitter", "oauth_token")
OAUTH_TOKEN_SECRET = config.get("twitter", "oauth_token_secret")
DISCOGS_TOKEN = config.get("discogs", "token")


twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

d = discogs_client.Client('ExampleApplication/0.1', user_token=DISCOGS_TOKEN)
results = d.list('117796')

# 15
for i in range(69, len(results.items)):
#for item in results.items:
    item = results.items[i]
    title = item.display_title
    url = item.url
    status = title + " \n " + url
    try:
        print("tweeting: ", status)
        twitter.update_status(status=status)
    except Exception as e:
        print("err: ", e)
    
    print("tweeted, now sleeping")
    time.sleep(1800)

