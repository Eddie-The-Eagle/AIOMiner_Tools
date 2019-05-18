#!/usr/bin/python3
#Created by Bobby Roberts Jr. 5/13/2019 for AIOMiner Discord
#Do whatever you want with this AIOMiner.com loves you :)

from twitter_scraper import get_tweets
from aiominer_discord import Webhook
import os
import re
from urllib.request import Request, urlopen

#Variables N Things
file_name='tweet.aio'
hook_url='{{DISCORD_WEBHOOK_HERE}}'
keyword='pow '


def purge_file():
    file = open(file_name,'w+')
    file.truncate(0)

def append_file(string):
    file = open(file_name,"w")
    file.write(string)
    file.close()


def check_file_for_string(string):
    if string in open(file_name).read():
       return True
    else:
       return False

def send_discord_msg(coin_msg):
    message = Webhook(hook_url,msg=coin_msg)
    message.post()
    #print (message)

#The thing
for tweet in get_tweets('ubiqannbot',pages=1):
    #Get the first one, we don't care about the rest, put this in a cron for every minute or 5.
    #Or fix this code to look at the time stamps of each or create a database of your very own
    #Made to be quick and dirty....this is usually how it all starts.  Next thing you know were adding
    #In trys, exceptions, 9.999999999% uptime SLA's, but for now....here we are
    AIOMiner=tweet['text'].encode('ascii', 'ignore').decode('ascii')
    if "[ANN]" in AIOMiner:
       #Check if we already know about this one, skip if we do
       if check_file_for_string(AIOMiner) == True:
          #We already have this, move on with your life
          exit()
       else:
          #We Have a new fish on the line!
          #Kill the text in the file
          purge_file()
          #Write the new one
          append_file(AIOMiner)
          #Gets the bitcointalk URL from Tweet
          url = re.findall('https://bitcointalk.*', AIOMiner)
          #Opens the URL and makes it readable
          req = Request(url[0], headers={'User-Agent': 'Mozilla/5.0'})
          web_byte = urlopen(req).read()
          webpage = web_byte.decode('utf-8', 'ignore')
          #Splits the webpage so we only get the first post
          webpage.split('</tr>', maxsplit=1)[0]
          if keyword in webpage.lower():
              #Send a Discord
              send_discord_msg("[PoW ] + str(AIOMiner))
          else:
              send_discord_msg("[No-PoW ] + str(AIOMiner))
          #We only care about the first one, get out of this situation
          exit()
