# -*- coding: utf-8 -*-
"""
The happiest state
"""
import sys
import json


def parse_tweets(source_file):
    lines = []
    for line in source_file.readlines():
        lines.append(json.loads(line))
    return lines
    
    
def main():
    with  open(sys.argv[1]) as tweet_file:
        tweets = parse_tweets(tweet_file)
        hashtags = {}
        for tweet in tweets:
            #get the hashtags and count
            print tweet
        
if __name__ == '__main__':
    main()
