# -*- coding: utf-8 -*-
"""
Top ten hash tags
"""
import sys
import json
import operator


def parse_tweets(source_file):
    lines = []
    for line in source_file.readlines():
        lines.append(json.loads(line))
    return lines
    
    
def main():
    with  open(sys.argv[1]) as tweet_file:
        tweets = parse_tweets(tweet_file)
        hashtag_count = {}
        for tweet in tweets:
            #get the hashtags and count
            if tweet.has_key('entities'):
                hashtags = tweet['entities'].get('hashtags', [])
                for ht in hashtags:
                    text = ht['text']
                    if hashtag_count.has_key(text):
                        hashtag_count[text] += 1
                    else:
                        hashtag_count[text] = 1
        sorted_hashtags = sorted(hashtag_count.iteritems(), key=operator.itemgetter(1))
        for key, value in reversed(sorted_hashtags[-10:]):
            print '%s %s' % (key, value)
        
if __name__ == '__main__':
    main()
