# Import the necessary package to process data in JSON format
try:
    import json
except ImportError:
    import simplejson as json

import sentiment
from dateutil import parser
import calendar
import gzip
import glob

filelist = glob.glob("../twitter_output_sf/2017/04/*.gz")

for filename in filelist:
    with gzip.open(filename, "rb") as tweets_file:
        try:
            for line in tweets_file:
                # Read in one line of the file, convert it into a json object
                tweet = json.loads(line.strip())
                if 'retweeted_status' not in tweet and 'text' in tweet and tweet['lang'] == "en":
                    # only messages contains 'text' field is a tweet and not retweet and in English
                    textlist = sentiment.filter(tweet["text"].encode('utf-8'))
                    emotion = sentiment.classifier.classify(sentiment.word_feats(textlist))
                    date = parser.parse(tweet["created_at"])
                    timestamp = calendar.timegm(date.timetuple())
                    id = tweet['id']
                    userid = tweet['user']['id']
                    print "{0}\t{1}\t{2}\t{3}\t{4}".format(userid,textlist,timestamp,id,emotion)
        except:
            # read in a line is not in JSON format (sometimes error occured)
            continue



#date = parser.parse(tweet["created_at"])
# transform datetime string to timestamp
#date.year #date.month
#timestamp = calendar.timegm(date.timetuple())
#from datetime import datetime
#datetime.utcfromtimestamp(1486978728)
#localtime:
#datetime.fromtimestamp(1486978728)

#python extract_sf.py > twitter_filter_sf.txt


