import tweepy
import os
import time
from datetime import datetime

DNX_BEARER_TOKEN = os.getenv("DNX_BEARER_TOKEN")
DNX_API_KEY = os.getenv("DNX_API_KEY")
DNX_API_SECRET_KEY = os.getenv("DNX_API_SECRET_KEY")
DNX_ACCESS_TOKEN = os.getenv("DNX_ACCESS_TOKEN")
DNX_ACCESS_TOKEN_SECRET = os.getenv("DNX_ACCESS_TOKEN_SECRET")

TWEET_FILE = 'tweets_dnx.txt'

client = tweepy.Client(
    bearer_token=DNX_BEARER_TOKEN,
    consumer_key=DNX_API_KEY,
    consumer_secret=DNX_API_SECRET_KEY,
    access_token=DNX_ACCESS_TOKEN,
    access_token_secret=DNX_ACCESS_TOKEN_SECRET
)

def post_tweet(tweet):
    try:
        client.create_tweet(text=tweet)
        print(f"Tweeted: {tweet}")
    except Exception as e:
        print(f"Error posting tweet: {e}")

def get_today_tweet():
    try:
        with open(TWEET_FILE, 'r') as file:
            tweets = file.readlines()
        
        day_of_year = datetime.now().timetuple().tm_yday
        tweet_index = (day_of_year - 1) % len(tweets)
        return tweets[tweet_index].strip()
    except Exception as e:
        print(f"Error reading tweet file: {e}")
        return None

if __name__ == '__main__':
    tweet = get_today_tweet()
    if tweet:
        post_tweet(tweet)