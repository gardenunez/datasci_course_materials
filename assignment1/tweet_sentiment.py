import sys
import json

def hw(tweet_file):
    tweets = parse_tweets(tweet_file)
    print len(tweets)

def lines(fp):
    print str(len(fp.readlines()))

def parse_tweets(source_file):
    lines = []
    for line in source_file.readlines():
        lines.append(json.loads(line))
    return lines

def main():
    try:
        sent_file = open(sys.argv[1])
        tweet_file = open(sys.argv[2])
        hw(tweet_file)
        lines(sent_file)
        #lines(tweet_file)
    finally:
        sent_file.close()
        tweet_file.close()

if __name__ == '__main__':
    main()
