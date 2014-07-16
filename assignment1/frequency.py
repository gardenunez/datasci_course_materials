# -*- coding: utf-8 -*-
"""
Compute Term Frequency
"""
import sys
import json

def compute_term_freq(tweets):
    term_occurrences = {}
    total_occurrences = 0.0
    for tweet in tweets:
        if tweet.has_key('text'):
            text = tweet['text'].lower()
            words = text.split()
            for wd in words:
                if term_occurrences.has_key(wd):
                    term_occurrences[wd] += 1
                else:
                    term_occurrences[wd] = 1
            total_occurrences += len(words)
    term_freq = {}
    for term, occurrence in term_occurrences.items():
        term_freq[term] = occurrence/total_occurrences
    return term_freq


def parse_tweets(source_file):
    lines = []
    for line in source_file.readlines():
        lines.append(json.loads(line))
    return lines


def main():
    with open(sys.argv[1]) as tweet_file:
        tweets = parse_tweets(tweet_file)
        term_freq = compute_term_freq(tweets)
        for term, freq in term_freq.items():
            print '%s %.4f' % ( term, freq)


if __name__ == '__main__':
    main()
