import tweepy
import os
import re

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

current_mentions = api.mentions_timeline()
for mention in current_mentions:
    if (approve_verify_pattern.match(mention.text)) and (mention.id not in answered_cache):
        print("Approving tweet " + str(mention.id))
        api.update_status("Подтверждаю @{}".format(mention.user.screen_name), in_reply_to_status_id=mention.id)
        answered_cache.add(mention.id)
    else:
        print("Tweet " + str(mention.id) + " already approved or has invalid approve message!")

store_to_cache(answered_cache)
