import pandas as pd
import re
import tweepy #tweepy (library to access twitter API)
import json
import numpy as np 
import time
import pickle


#below are the credentials obtained by requesting, to use twitter API. 
#get your own api keys @https://developer.twitter.com/en
consumer_key = r"XXXXXXXXXXXXXXXXXXXXXXXXXX"
consumer_secret = r"XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
access_token = r"XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
access_token_secret = r"XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" 

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def user_tweets(screen_name):
  all_tweets_info = tweepy.Cursor(api.user_timeline, screen_name = screen_name, tweet_mode='extended').items(200) 
  #number of tweets you want to extract, here = 200 
  #Note the free API access from twitter allows limited number of tweets to be extracted. For more details visit twitter API documentation
  searched_tweets = [status for status in all_tweets_info]

  COLS = {"tweet_id", 'tweet_created_at', 'tweet_lang', 'tweet_source', "tweet_hashtags", "tweet_user_mentions_id",
          "tweet_full_text", "user_id_str", 'user_screen_name', 'user_name', "user_profile_description", "user_statuses_count",
          'user_followers_count', "user_friends_count", "user_listed_count", "user_verified", "user_time_zone", "geo_enabled", 
          "user_timeline_lang", "geo", 'user_location', "user_profile_created_at", "place_coordinates", "place_id", "place_type",
          "place_country_code", "place_name", "coordinates"
          }
  #len = 28 cols.  
  df =  pd.DataFrame(columns = COLS) 

  for tweet in searched_tweets:
    df = df.append({"tweet_id" : tweet.id_str,
                    'tweet_created_at' : tweet.created_at,
                    'tweet_lang' : tweet.lang,
                    'tweet_source' : tweet.source, 
                    'tweet_hashtags' : [e['text'].encode('utf-8') for e in tweet._json['entities']['hashtags']],
                    "tweet_user_mentions_id" : [e["id_str"] for e in tweet.entities["user_mentions"]],
                    "tweet_full_text" : tweet.full_text.replace("\n"," ").encode('utf-8'),
                    "user_id_str" : tweet.user.id_str,
                    'user_screen_name' : tweet.user.screen_name.encode('utf-8'),
                    'user_name' : tweet.user.name.encode('utf-8'), 
                    'user_profile_description' : tweet.user.description.encode('utf-8'), 
                    'user_statuses_count' : tweet.user.statuses_count,
                    'user_followers_count' : tweet.user.followers_count,
                    'user_friends_count' : tweet.user.friends_count,
                    'user_listed_count' : tweet.user.listed_count,
                    'user_verified' : tweet.user.verified,  
                    'user_time_zone' : tweet.user.time_zone, 
                    'geo_enabled' : tweet.user.geo_enabled,
                    'user_timeline_lang' :tweet.user.lang,
                    'geo' : tweet.geo,                 
                    'user_location' : tweet.user.location.encode('utf-8'),
                    'user_profile_created_at' : tweet.user.created_at,
                    "place_coordinates" : (tweet.place if tweet.place==None else tweet.place.bounding_box.coordinates),
                    "place_id" : (tweet.place if tweet.place==None else tweet.place.id),
                    "place_type" : (tweet.place if tweet.place==None else tweet.place.place_type),
                    "place_country_code" : (tweet.place if tweet.place==None else tweet.place.country_code),
                    "place_name": (tweet.place if tweet.place==None else tweet.place.full_name)
                    'coordinates' : tweet.coordinates,
                    }, ignore_index = True)
    
    return df
    
screen_name = "iamsrk"
srk_df = user_tweets(screen_name)
srk_df.to_csv("%s.csv" %(screen_name)) 
