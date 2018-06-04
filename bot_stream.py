import tweepy
import re
import os
import time

from secrets import *
from bot_token import *

cache_file_name = 'answered_tweets_cache.txt'


def store_to_cache(cache_set):
    if not os.path.exists('cache'):
        os.makedirs('cache')
    with open('cache/' + cache_file_name, 'w') as f:
        for item in cache_set:
            f.write("%s\n" % item)


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
current_user = api.verify_credentials()
print("Currently logged in as: " + current_user.name)

approve_verify_pattern = re.compile(".*@{}.*подтверди.*".format(current_user.screen_name))

answered_cache = set()
try:
    with open('cache/' + cache_file_name, 'r') as cache_file:
        for line in cache_file.readlines():
            answered_cache.add(int(line.rstrip('\n').rstrip('\r')))
except OSError:
    print("Cache file is missing, skipping for now")


class BotStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        if (approve_verify_pattern.match(status.text)) and (status.id not in answered_cache):
            print("Status recieved, waiting before answer")
            time.sleep(15)
            print("Approving tweet " + str(status.id))
            api.update_status("Подтверждаю @{}".format(status.user.screen_name), in_reply_to_status_id=status.id)
            answered_cache.add(status.id)
            store_to_cache(answered_cache)
        else:
            print("Tweet " + str(status.id) + " already approved or has invalid approve message!")


bot_stream = tweepy.Stream(auth=api.auth, listener=BotStreamListener())
bot_stream.filter(track=['@' + current_user.screen_name])
