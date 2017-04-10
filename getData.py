import tweepy
import json
import oauth2
import argparse
import os
import re
import HTMLParser

def parse_config():
    config = {}
    # from file args
    if os.path.exists('config.json'):
        with open('config.json') as f:
              config.update(json.load(f))
    else:
          # may be from command line
          parser = argparse.ArgumentParser()

          parser.add_argument('-ck', '--consumer_key', default=None, help='Your developper `Consumer Key`')
          parser.add_argument('-cs', '--consumer_secret', default=None, help='Your developper `Consumer Secret`')
          parser.add_argument('-at', '--access_token', default=None, help='A client `Access Token`')
          parser.add_argument('-ats', '--access_token_secret', default=None, help='A client `Access Token Secret`')

          args_ = parser.parse_args()
          def val(key):
            return config.get(key)\
                   or getattr(args_, key)\
                   or raw_input('Your developper `%s`: ' % key)
          config.update({
            'consumer_key': val('consumer_key'),
            'consumer_secret': val('consumer_secret'),
            'access_token': val('access_token'),
            'access_token_secret': val('access_token_secret'),
          })
    return config

class ProcessTweets:

    # Preprocess the tweets
    def preProcessTweet(self, tweet):
        # Convert to lower case
        tweet = tweet.lower()
        # Remove the html escape chars
        tweet = HTMLParser.HTMLParser().unescape(tweet)
        # Removing the emojis
        emoji_pattern = re.compile(
                    u"(\ud83d[\ude00-\ude4f])|"  # emoticons
                    u"(\ud83c[\udf00-\uffff])|"  # symbols & pictographs (1 of 2)
                    u"(\ud83d[\u0000-\uddff])|"  # symbols & pictographs (2 of 2)
                    u"(\ud83d[\ude80-\udeff])|"  # transport & map symbols
                    u"(\ud83c[\udde0-\uddff])"  # flags (iOS)
                    "+", flags=re.UNICODE)
        tweet = emoji_pattern.sub(r'', tweet)               # no emoji
        #Convert https?://* to URL
        tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)
        #Convert @username to AT_USER
        tweet = re.sub('@[^\s]+','AT_USER',tweet)    
        #Remove additional white spaces
        tweet = re.sub('[\s]+', ' ', tweet)
        #Replace #word with word
        tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
        #trim
        tweet = tweet.strip()
        #remove first/last " or 'at string end
        tweet = tweet.rstrip('\'"')
        tweet = tweet.lstrip('\'"')
        return tweet
        
    
class StoreData:
    def __init__(self):
        self.savepath = os.path.join(os.getcwd(),'data','tweets')
        self.fileName = os.path.join(self.savepath,'politics.txt')
        self.fileOb = open(self.fileName,'a')

    def storedata(self,tweet):
        try:
            self.fileOb.write(tweet+'\n')
        except UnicodeEncodeError:
            print('Unicode Error occured')

store = StoreData()
processT = ProcessTweets()

class StreamListener(tweepy.StreamListener):
    def on_status(self,status):
        
        if (not status.retweeted) and ('RT @' not in status.text) :
            tweet = status.text
            print('Original:\n'+tweet)
            tweet = processT.preProcessTweet(tweet)
            print('Processed:\n'+tweet)
            store.storedata(tweet)
            
            
    def on_error(self, status_code):
        if status_code == 420:
            return False


def main():
    config = parse_config()
    auth = tweepy.OAuthHandler(config.get('consumer_key'),config.get('consumer_secret'))
    auth.set_access_token(config.get('access_token'),config.get('access_token_secret'))
    api = tweepy.API(auth)
    
    stream_listener = StreamListener()
    stream = tweepy.Stream(auth=api.auth,listener=stream_listener)
    keywords = raw_input('Enter keywords: ').split()
    stream.filter(track=keywords,languages=['en'])

main()
