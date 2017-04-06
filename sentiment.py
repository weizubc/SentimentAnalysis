import pandas as pd
import re

traindata = pd.read_csv('training.csv',header=None)
testdata = pd. read_csv('test.csv',header=None)

negtrain = traindata[traindata[0]==0][5]
negtrain.index= range(len(negtrain))

postrain = traindata[traindata[0]==4][5]
postrain.index= range(len(postrain))

negtest = testdata[testdata[0]==0][5]
negtest.index= range(len(negtest))

postest= testdata[testdata[0]==4][5]
postest.index= range(len(postest))

def split_string(source,splitlist):
    output = []
    atsplit = True
    for char in source:
        if char in splitlist:
            atsplit = True
        else:
            if atsplit:
                output.append(char)
                atsplit = False
            else:
                output[-1] = output[-1] + char
    return output

def filter(tweet):
    sub = re.sub(r'http(s)?://[\w./-]+',r'URL',tweet)
    sub = re.sub(r'@[\w]+',r'USERNAME',sub)
    word_list = [e.lower() for e in split_string(sub,'\n.;,: ') if len(e) >= 3]
    for i in range(len(word_list)):
        count = 0
        oldchar = None
        newword = ''
        for char in word_list[i]:
            if oldchar and char != oldchar:
                if count == 1:
                    newword = newword + oldchar
                else:
                    newword = newword + oldchar + oldchar
                count = 0
            oldchar = char
            count += 1
        if count == 1:
            newword = newword + oldchar
        else:
            newword = newword + oldchar + oldchar
        word_list[i] = newword
    return word_list



tweets = []
for i in range(len(negtrain)):
    words_filtered = filter(negtrain[i])
    tweets.append((words_filtered, 'neg'))

for i in range(len(postrain)):
    words_filtered = filter(postrain[i])
    tweets.append((words_filtered, 'pos'))


test_tweets = []
for i in range(len(negtest)):
    words_filtered = filter(negtest[i])
    test_tweets.append((words_filtered, 'neg'))

for i in range(len(postest)):
    words_filtered = filter(postest[i])
    test_tweets.append((words_filtered, 'pos'))



import nltk.classify.util
from nltk.classify import NaiveBayesClassifier

def word_feats(words):
    return dict([(word, True) for word in words])

trainfeats = [(word_feats(tweet), sentiment) for (tweet,sentiment) in tweets]
testfeats = [(word_feats(tweet), sentiment) for (tweet,sentiment) in test_tweets]

print 'train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats))

classifier = NaiveBayesClassifier.train(trainfeats)
print 'accuracy:', nltk.classify.util.accuracy(classifier, testfeats)

#classifier.show_most_informative_features()

#tweet="I haven't received my stimulus yet"
#print classifier.classify(word_feats(filter(tweet)))



