# -*- coding: utf-8 -*-

import sys
import json
from nltk.util import ngrams

MAX_NGRAMS_DEGREE = 3

MOCK_TWEETS = [{'text':"can't stand in love"}, \
        {'text':'the cool stuff is not that cool'}, \
        {'text':"cashing in and love me, but dont like me"}, \
        {"text":"it does not work. fix it up!!"}, \
        {'text':"I was naïve once-in-a-lifetime , \
        now I'm self-confident and walk in right direction"}, \
        {"text":"no fun, no screwed, screwed up. dont like!!! , like."}]

def trim_tweet_text(text):
    result = ""
    g  = lambda c: c.isalnum() or c in [u'-', u"'"]
    for char in text:
        try:
            if g(char):
                result = "%s%s" % (result, char)
            else:
                result = "%s " % result
        except UnicodeDecodeError:
            continue
    return result

def get_sentiments(tweets, scores):
    for tweet in tweets:
        if tweet.has_key('text'):
	    text = tweet['text']
            text = trim_tweet_text(text)
            splitted_text = text.split()
            score_map = {}
	    degree = range(min(len(splitted_text),MAX_NGRAMS_DEGREE) + 1, 0, -1)
            ignore_words = []
	    for g in degree:
	        ng = ngrams(splitted_text, g)
		for words in ng:
		    term = ' '.join(words)
		    if scores.has_key(term):
                        #if multiple words term, ignore this ones if appears again
                        if len(words) > 1:
                            ignore_words.extend(words) 
                        elif term in ignore_words:
                            ignore_words.remove(term)
                            continue
		        if score_map.has_key(term):
                            score_map[term] += 1
                        else:
                            score_map[term] = 1
	    score = sum([scores[key] * value for key, value in score_map.items()])
            print score

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
    return scores

def main():
    try:
        sent_file = open(sys.argv[1])
        tweet_file = open(sys.argv[2])
        scores = parse_sentiment_file(sent_file)
        tweets = parse_tweets(tweet_file)
        get_sentiments(tweets, scores)
	#get_sentiments(MOCK_TWEETS, scores)
    finally:
        sent_file.close()
        tweet_file.close()

if __name__ == '__main__':
    main()
