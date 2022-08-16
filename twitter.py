import tweepy
import os
from dotenv import load_dotenv
from time import sleep

load_dotenv()  # Check Environment Variables in .env file
twitter_api = os.getenv('TWITTER_API')
twitter_secret = os.getenv('TWITTER_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
access_secret = os.getenv('ACCESS_SECRET')
bearer_token = os.getenv('BEARER_TOKEN')

auth = tweepy.OAuthHandler(twitter_api, twitter_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.Client(bearer_token, twitter_api, twitter_secret, access_token, access_secret,
                    wait_on_rate_limit=True)


def tweet(tokens, amount, vaults):
    amount = int(amount)
    line1 = f"🚨 {amount/10**vaults[tokens]['decimals']:,.2f}  $USDC are available to be deposited on the #UMAMI {vaults[tokens]['title']} ! 🚨"
    line2 = f"💸 {vaults[tokens]['website']} 💸"
    message = '\n \n'.join([line1, line2])
    if len(message) < 280:
        try:
            api.create_tweet(text=message)
            print("tweet sent!")
        except tweepy.TweepyException as e:
            print(e.api_messages)
        except:
            print("error sending tweet")
    else:
        print("tweet too long")
    sleep(5)
