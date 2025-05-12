import tweepy
import os
import time
from datetime import datetime

BEARER_TOKEN = os.getenv("BEARER_TOKEN")
API_KEY = os.getenv("API_KEY")
API_SECRET_KEY = os.getenv("API_SECRET_KEY")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

TWEET_FILE = 'tweets.txt'

client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=API_KEY,
    consumer_secret=API_SECRET_KEY,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
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