# -*- coding: utf-8 -*-

import sys
from urllib import urlencode
import requests
from urlparse import urlparse, parse_qs
from random import choice
import re
from datetime import datetime, date, time
import calendar

#settings

#your birthday: datetime(year, month, day[, hour[, minute[, second[, microsecond[, tzinfo]]]]])
bday = datetime(2016, 12, 7, 12, 30, 0)

#access_token: Generate one at https://developers.facebook.com/tools/explorer
# access_token = "EAACEdEose0cBAHeXbrFrar4mxxuLbGEQseune7UZC6UxeV5Io9BkTrmHDxyMZCABeIjn215f9ZBmyybXnCINkUX4oXE4mROVPXkKweNKlKE0qTJfXwo1av2rDl3FgRPU5ISK131fF3kCm0rzvFiaTlYvlZC5zy7yGmHit10T8QZDZD"
access_token = "EAACEdEose0cBAELDou62ojrCOWw9PqZCRZBS1YzH2gg4CJtXLZCeNBiJfVVewLDiEQMGHyhHGfcEFPLLiMZAu5sAVSvR9HecJCzGyZB0jqPxoDpzhrpXG8Sal48bTii1XAdHUVwlZBtD9I1boqGHDm3ZCwunpUYdOzB5j5NOIv8kQZDZD"
#set true to like posts on your wall
like = True;

#set true to comment thank you
comment = True;

#the list of messages from which you want a random message to be selected
# message_set = ['Thank you very much', 'Thanks a lot', 'Thank you!']
message_set = ['Your wishes have become a keepsake that will forever remind me of happy times and beautiful memories. Thanks.',
                'Your beautiful wishes did something that no amount of money can buy they made me believe in the value of friendship. Thanks!',
                'Your wishes made my day is what I want you to know. For a long time in my heart, your words will echo. Thanks.',
                'Gifts will wither away into the sands of time, but your words will reverberate in my heart forever, like a sweet little rhyme. Thanks.',
                'Gifts' "can\'t" "be carried around but I will carry the essence of your beautiful message wherever I go. Thank you.",
                'Thank you so much.']

#if false, repies to every message. Make it false if you are sure every wish posted on your wall is a birthday message
use_filter = True

#keywords to respond to. Comment only on posts containing at lease one of these words
bdaywords = ["Happy", "Anuj", "Anujraaj" ,"Goyal", "HBD", "hbd", "bdae", "happy", "you", "many", "Many",  "bdae", "love","Birthday","wishes","Wishes" "Goel", "bday", "b\'day", "birthday", "wish", "returns","anniversaire","compleanno","Geburtstag","natalis"]

#proxy settings
http_proxy = "https://iim2014002:Anuj9811410760@172.31.1.4:8080"
http_proxy = "http://iim2014002:Anuj9811410760@172.31.1.4:8080"
ftp_proxy = "iim2014002:Anuj9811410760@172.31.1.4:8080"

#do not change anything beyond this line

#calculate utc timestamp
epoch=datetime(1970,1,1)
td = bday - epoch
utc_bday = int((td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 1e6)

#create proxy dictionary
proxy_dict = {
    "http" : http_proxy,
    "https" : http_proxy,
    "ftp" : ftp_proxy
}

#get birthday wishes
def get_posts(url, wishes=None):
    #check if we are done
    if wishes is None:
        wishes = []
        stop = False
    else:
        until = parse_qs(urlparse(url).query).get('until')
        stop = int(until[0]) < utc_bday

    if ('paging' not in requests.get(url, proxies=proxy_dict).json() ):
        stop = True

    if stop:
        return wishes
    else:
        print url
        req = requests.get(url, proxies=proxy_dict)
        if req.status_code == 200:
            content = req.json()
            
            #keep only relevant fields from post data
            feed = []
            for post in content['data']:
                print 'content'

                if('comments' not in post):
                    print post
                    feed.append({'id': post['id'],'from': post['from']['name'],'message': post.get('message', ''),'type': post['type']})

            #keep only posts relevant to birthday. Make sure you reply your friends who post happy birthday pictures on your timeline or posts in local language
            print 'feed'
            print feed
            for post in feed:
                if post['type']=='status' and is_birthday(post['message'], use_filter) :
                    wishes.append(post)

            next_url = content['paging']['next']
            return get_posts(next_url, wishes)
        else:
            print "Unable to connect. Check if session is still valid"

def confirm(prompt=None, resp=False):
    if prompt is None:
        prompt = 'Confirm'
    if resp:
        prompt = '%s [%s]|%s: ' % (prompt, 'y', 'n')
    else:
        prompt = '%s [%s]|%s: ' % (prompt, 'n', 'y')
    while True:
        ans = raw_input(prompt)
        if not ans:
            return resp
        if ans not in ['y', 'Y', 'n', 'N']:
            print 'please enter y or n.'
            continue
        if ans == 'y' or ans == 'Y':
            return True
        if ans == 'n' or ans == 'N':
            return False

def is_birthday (message, filter):
    if filter == False:
        return True
    for keyword in bdaywords:
        if keyword in message:
            return True
    return False

if __name__ == '__main__':
    
    while(1):
        #get bithday wishes
        # base_url = 'https://graph.facebook.com/v2.3/me/feed'
        # params = {'since': utc_bday,'access_token': access_token}
        # url = '%s?%s' % (base_url, urlencode(params))
        # url = 'https://graph.facebook.com/v2.3/me/feed?access_token=EAACEdEose0cBAFFknK0L48RDnsdZCpxV2cyLymFADZAiESx0qjyct1QAvvm93xAoshCr6mkAD8CU0gFIr8zZC6gjMN0hZAVRB2aZCQZBYoo3jlwcpscJVJE555vym7Fhbd1f5BezLgzah8qUF4kr7GcN1GsryZCBvPj3JIe3l4KRgZDZD&fields=id,name,message,from,type,comments'
        # ubday = (str)utc_bday
        url = "https://graph.facebook.com/v2.8/me/feed?fields=id%2Cname%2Cmessage%2Cfrom%2Ctype%2Ccomments&since="+str(utc_bday)+"&access_token="+access_token
        # url = "https://graph.facebook.com/v2.8/me/feed?fields=id%2Cname%2Cmessage%2Cfrom%2Ctype%2Ccomments&access_token=EAACEdEose0cBADHWXZCvjv8JZABm6G786ZBoGZBxNDEIAVohW4zB5BbEPiCzNC0bnYwqtvxDWHp0ZAPKufiazqO4Dk26F4dbxAyTNzcmjMRhco7i6QZAkO2wp4uuJN0pjOFZBF5upjvWwNiym1OvcoUZACiZBVuptIeyhIGnCJLx2dQZDZD"
        posts = get_posts(url)
        
        #confirm before posting
        print 'blah'
        print posts
        # usersignal = confirm('Found %s birthday wishes. Ready to thank them?' % (len(posts)))
        usersignal = True
        #post if user said yes
        if usersignal is True:
            for post in posts:
                # /v2.3/{object-id}/comments
                #thank the user
                if comment:
                    reply = choice(message_set)
                    # reply = 'y'
                    print 'Replying %s to %s' % (reply, post['from'])
                    url = 'https://graph.facebook.com/v2.3/%s/comments?access_token=%s' % (post['id'], access_token)
                    print requests.post(url, data={'message': reply}, proxies=proxy_dict)

                if like:
                    url = 'https://graph.facebook.com/v2.3/%s/likes?access_token=%s' % (post['id'], access_token)
                    print requests.post(url, data="", proxies=proxy_dict)