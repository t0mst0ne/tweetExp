__author__ = 'kimi, modified by summit'

from twitter import *
import time
import dateutil.parser
from elasticsearch import Elasticsearch

CONSUMER_KEY = "rLsrAkuJSETe77RqicDtTQnzc"
CONSUMER_SECRET = "xjWfVkVPE3xHyOD8lCwJ8nC8U54agdysZ6OjkZoZEcccwBuGOk"
ACCESS_KEY = "591945759-ri4RI0WvGEw24dIkSzqkrcSF8QuQxWCKd5sgjuPC"
ACCESS_SECRET = "NfuvaK8ADtRUfkyeS44Y5gTOQZe8Mld41legYlp6O0wlO"

es = Elasticsearch("104.236.193.82:9200")

# create twitter API object
auth = OAuth(ACCESS_KEY, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
stream = TwitterStream(auth = auth, secure = True)

# iterate over tweets matching this filter text
# IMPORTANT! this is not quite the same as a standard twitter search
#  - see https://dev.twitter.com/docs/streaming-api
tweet_iter = stream.statuses.filter(track = "baseball, mlb")

for tweet in tweet_iter:
    # check whether this is a valid tweet
    if tweet.get('text'):
        # yes it is! print out the contents, and any URLs found inside
        #print "(%s) @%s %s" % (tweet["created_at"], tweet["user"]["screen_name"], tweet["text"])
        ts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
        ts = dateutil.parser.parse(ts)
        ts = ts.isoformat()
        #print(ts)

        res = es.index(
            index="twi-mlb", doc_type=ts, id=ts, body={
                'timestamp':ts,
                'text':tweet["text"]
            })

        #x = tweet["text"].split()
        #print x

        #for url in tweet["entities"]["urls"]:
        #    print " - found URL: %s" % url["expanded_url"]
