import sys
import json

def hw(tweet_file):
    tweets = parse_tweets(tweet_file)
    print len(tweets)

def parse_tweets(source_file):
    lines = []
    for line in source_file.readlines():
        lines.append(json.loads(line))
    return lines

def parse_sentiment_file(sent_file):
    """
    Parse the sentiment file.
    return: dict
    """
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
        print tweets
    finally:
        sent_file.close()
        tweet_file.close()

if __name__ == '__main__':
    main()
