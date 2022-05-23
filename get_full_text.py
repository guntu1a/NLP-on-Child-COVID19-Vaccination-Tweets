import tweepy
import csv
import datetime
import json
import os


consumer_key = 'pRw4PPuHLWje40Hqqe2Z53pRT'
consumer_secret = 'kLc35kiCf5rV2xK40Or3FkyXa5G388IrHRMPm9KWhgdL0xX9Yo'
access_token = '16479615-1QhMcQjHz5bwqiJGEWTEu08LitnPotme2RWVfpZ2S'
access_token_secret = '8oBpfnGUywzgSBdSYvvdQG7dTJ4QlUQcXFrQI72nSESRr'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

##id = 1272771459249844224
##status = api.get_status(id)
##text = status.text 
##print(text)

field_names = []
fOut = open('/Users/gandy1l/Desktop/research/vaccine_child/cleaned_full_text_child2.csv','w')
dTweet = {}

with open('/Users/gandy1l/Desktop/research/vaccine_child/cleaned_with_orig_tweet_only_child.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    field_names = reader.fieldnames
    writer = csv.DictWriter(fOut, fieldnames=field_names)
    writer.writeheader()

    i=0
    for row in reader:
        i+=1
        if i>3424:
            break
            

        reply_id = row['id']
        if(len(reply_id) < 10): #not None, sloppy way to do it :)
            continue
        reply_id = reply_id.replace('"','')
       
        tweet_id = row['in_reply_to_status_id_str']
        if(len(tweet_id) < 10): #not None, sloppy way to do it :)
            continue
        tweet_id = tweet_id.replace('"','')
        tweet_id.strip()
        print(tweet_id)
        text = ""
        if tweet_id in dTweet.keys():
            print('already found')
            text = dTweet[tweet_id]
        else:
            try:
                print('new one')
                status = api.get_status(tweet_id,tweet_mode="extended")
                text = status.full_text
                dTweet[tweet_id] = text
            except Exception as ex:
                print(ex)
                print ('problem')
                continue

        try:
            status = api.get_status(reply_id,tweet_mode="extended")
            reply_text = status.full_text
        except Exception as ex:
            print(ex)
            continue
        
        dOut = row
        dOut['original_tweet_text'] = text
        dOut['text'] = reply_text
        writer.writerow(dOut)
        
        

