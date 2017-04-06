#!/usr/bin/python

import sys
from datetime import datetime

oldkey = []
#count = 0
oldtime = 0

for line in sys.stdin:
    data = line.strip().split("\t")
    if len(data) == 5:
        userid, textlist, timestamp, id, emotion = data
    thiskey = []
    thiskey.append(userid)
    thiskey.append(textlist)
    thistime = int(timestamp)
    date = datetime.fromtimestamp(thistime)


    if oldkey == thiskey and thistime - oldtime < 3600:
        # Repeat Tweets (the same text within one hour). Skip this line.
        continue
    else:
        print "{0}\t{1}\t{2}\t{3}\t{4}\t{5}".format(date.year,date.month,date.day,date.hour,emotion,date.weekday())
        #count += 1
        oldkey = []
        oldkey.append(userid)
        oldkey.append(textlist)
        oldtime = thistime


#print count


#date = parser.parse(tweet["created_at"])
# transform datetime string to timestamp
#date.year #date.month
#timestamp = calendar.timegm(date.timetuple())
#from datetime import datetime
#datetime.utcfromtimestamp(1486978728)
#localtime:
#datetime.fromtimestamp(1486978728)




#cat twitter_filter_wikipedia.txt | sort |./mapper.py | sort |./reducer.py
#cat twitter_filter_sf.txt | sort |./mapper.py | sort |./reducer.py > result_sf.txt
