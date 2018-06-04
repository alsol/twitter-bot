import tweepy
import webbrowser

from secrets import *

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

# Get request token
redirect_url = auth.get_authorization_url()
print("Redirect url: " + redirect_url)
print("Proceed to twitter, then input your verify code below")

webbrowser.open(redirect_url)

# Get access code
verifier = input("Your verify code: ").strip()
try:
    auth.get_access_token(verifier)
except tweepy.TweepError:
    print('Error! Failed to get access token.')
    exit(1)

# Save token somewhere
save_file_name = "bot_token.py"
print("Printing tokens to \"{}\"".format(save_file_name))
with open(save_file_name, 'w') as f:
    print("access_token = \"{}\"".format(auth.access_token), file=f)
    print("access_token_secret = \"{}\"".format(auth.access_token_secret), file=f)

print("Auth done.")
