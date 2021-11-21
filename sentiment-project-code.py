# -*- coding: utf-8 -*-
"""
Created on Sun Sep 19 10:59:11 2021

@author: piyush
"""
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import matplotlib.pyplot as plt
def clean_tweet(tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
def get_tweet_sentiment(tweet):
    '''
    Utility function to classify sentiment of passed tweet
    using textblob's sentiment method
    '''
    # create TextBlob object of passed tweet text
    analysis = TextBlob(clean_tweet(tweet))
    # set sentiment
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'
def get_tweets(query, count):
# empty list to store parsed tweets
    tweets = []
    
    # call twitter api to fetch tweets
    #print(count)
    fetched_tweets = api.search_tweets(q=query,count=count)

    # parsing tweets one by one
    for tweet in fetched_tweets:
        # empty dictionary to store required params of a tweet
        parsed_tweet = {}

        # saving text of tweet
        parsed_tweet['text'] = tweet.text
        # saving sentiment of tweet
        parsed_tweet['sentiment'] = get_tweet_sentiment(tweet.text)

        # appending parsed tweet to tweets list
        if tweet.retweet_count > 0:
            # if tweet has retweets, ensure that it is appended only once
            if parsed_tweet not in tweets:
                tweets.append(parsed_tweet)
        else:
            tweets.append(parsed_tweet)

            # return parsed tweets
    return tweets
consumer_key = 'DaKOy4NkVRwMcXwjTmVo61T7r'
consumer_secret = 'U0RzRYPR4Hh2BNYVli68cRtUWkLM5RjHQpTfJTUtiYoTFAs27g'
access_token = '1461766889848205316-CRAFDbWxDXs7lR4KZeLibyMdjHnToN'
access_token_secret = 'gWNnDGG5IyLCRuTBKfHbV4uPs5wLMYeMSiPuJ2D4zG60P'

# attempt authentication
try:
    # create OAuthHandler object
    auth = OAuthHandler(consumer_key, consumer_secret)
    # set access token and secret
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    print("success")
except:
    print("Error: Authentication Failed")

#model starts
query = input("What to search for? ")
count = input("Enter how many tweets to analyze")
tweets = get_tweets(query, count)
# picking positive tweets from tweets
positive_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
negative_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
neutral_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'neutral']
print("number of positive tweets:",len(positive_tweets))
print("number of negative tweets:",len(negative_tweets))
print("number of neutral tweets:",len(neutral_tweets))
# percentage of positive tweets
print("Positive tweets percentage: {} %".format(100 * len(positive_tweets) / len(tweets)))
# f.write(format(100*len(ptweets)/len(tweets)))
# picking negative tweets from tweets

# percentage of negative tweets
print("Negative tweets percentage: {} %".format(100 * len(negative_tweets) / len(tweets)))
# percentage of neutral tweets
print("Neutral tweets percentage: {} %".format((100 * len(neutral_tweets) / len(tweets))))

# printing first 5 positive tweets
print("\n\nPositive tweets:")
for tweet in positive_tweets[:10]:
    print(tweet['text'])

    # printing first 5 negative tweets
print("\n\nNegative tweets:")
for tweet in negative_tweets[:10]:
    print(tweet['text'])
    # f.close()
print("\n\nNeutral tweets:")
for tweet in neutral_tweets[:10]:
    print(tweet['text'])
slices_tweets = [format(100 * len(positive_tweets) / len(tweets)), format(100 * len(negative_tweets) / len(tweets)),
                 format(100 * len(neutral_tweets) / len(tweets))]
analysis = ['Positive', 'Negative', 'Neutral']
colors = ['g', 'r', 'y']

plt.pie(slices_tweets, labels=analysis, startangle=-40, autopct='%.1f%%')
plt.savefig(query)
plt.show()