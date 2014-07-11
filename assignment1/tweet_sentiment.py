# -*- coding: utf-8 -*-

import sys
import json
from nltk.util import ngrams

MAX_NGRAMS_DEGREE = 3

#TODO: 1 - remove invalid characters in tweet's text valid characters: alpha , ', - , ï
#      2 - cool sutff should count only as "cool stuff" not like "cool" and "cool stuff" 

def get_sentiments(tweets, scores):
    for tweet in tweets:
        if tweet.has_key('text'):
	    text = tweet['text'].split()
	    score = 0
	    print 80*'*'
	    print text
	    degree = range(1, min(len(text),MAX_NGRAMS_DEGREE) + 1)
	    print degree
	    for g in degree:
	        ng = ngrams(text, g)
		for words in ng:
		    term = ' '.join(words)
		    #print term
		    if scores.has_key(term):
		        print term, scores[term]
		        score += scores[term]
            print tweet['text'], score

def parse_tweets(source_file):
    lines = []
    for line in source_file.readlines():
        lines.append(json.loads(line))
    return lines

def parse_sentiment_file(sent_file):
    scores = {} # initialize an empty dictionary
    for line in sent_file:
        term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scores[term] = int(score)  # Convert the score to an integer.
	#if not term.isalnum():
        #    print term
    return scores

def main():
    try:
        sent_file = open(sys.argv[1])
        tweet_file = open(sys.argv[2])
        scores = parse_sentiment_file(sent_file)
        #tweets = parse_tweets(tweet_file)
	mock_tweets = [{'text':"can't stand in love"}, \
                {'text':'the cool stuff is not that cool'}, \
                {'text':"cashing in and love me, but dont like me"}, \
                {"text":"it does not work . fix it up!!"}, \
                {'text':"I was naïve once-in-a-lifetime , \
                now I'm self-confident and walk in right direction"}]
	get_sentiments(mock_tweets, scores)
    finally:
        sent_file.close()
        tweet_file.close()

if __name__ == '__main__':
    main()
