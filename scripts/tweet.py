import tweepy
import os
import time
import smtplib
from datetime import datetime
from email.message import EmailMessage

BEARER_TOKEN = os.getenv("BEARER_TOKEN")
API_KEY = os.getenv("API_KEY")
API_SECRET_KEY = os.getenv("API_SECRET_KEY")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

DNX_BEARER_TOKEN = os.getenv("DNX_BEARER_TOKEN")
DNX_API_KEY = os.getenv("DNX_API_KEY")
DNX_API_SECRET_KEY = os.getenv("DNX_API_SECRET_KEY")
DNX_ACCESS_TOKEN = os.getenv("DNX_ACCESS_TOKEN")
DNX_ACCESS_TOKEN_SECRET = os.getenv("DNX_ACCESS_TOKEN_SECRET")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TWEET_FILE = 'tweets.txt'
DNX_TWEET_FILE = 'tweets_dnx.txt'

client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=API_KEY,
    consumer_secret=API_SECRET_KEY,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

dnx_client = tweepy.Client(
    bearer_token=DNX_BEARER_TOKEN,
    consumer_key=DNX_API_KEY,
    consumer_secret=DNX_API_SECRET_KEY,
    access_token=DNX_ACCESS_TOKEN,
    access_token_secret=DNX_ACCESS_TOKEN_SECRET
)

def send_email(subject, body):
    EMAIL_ADDRESS = os.getenv("EMAIL_USER")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASS")
    RECEIVER_EMAIL = "hello@datanautx.com"

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = RECEIVER_EMAIL
    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("Notification email sent.")
    except Exception as e:
        print(f"Failed to send email: {e}")

def post_tweet(tweepyClient, tweet):
    try:
        tweepyClient.create_tweet(text=tweet)
        print(f"Tweeted: {tweet}")
        send_email("✅ Tweet Success", f"The tweet was posted successfully:\n\n{tweet}")
    except Exception as e:
        print(f"Error posting tweet: {e}")
        send_email("❌ Tweet Failed", f"Tweet failed:\n\n{tweet}\n\nError: {e}")

def get_today_tweet(filename):
    try:
        with open(filename, 'r') as file:
            tweets = file.readlines()
        
        day_of_year = datetime.now().timetuple().tm_yday
        tweet_index = (day_of_year - 1) % len(tweets)
        return tweets[tweet_index].strip()
    except Exception as e:
        print(f"Error reading tweet file: {e}")
        return None

if __name__ == '__main__':
    tweet = get_today_tweet(os.path.join(SCRIPT_DIR, TWEET_FILE))
    if tweet:
        post_tweet(client, tweet)

    dnx_tweet = get_today_tweet(os.path.join(SCRIPT_DIR, DNX_TWEET_FILE))
    if dnx_tweet:
        post_tweet(dnx_client, dnx_tweet)