# -*- coding: utf-8 -*-
"""
The happiest state
"""
import sys
import json
from nltk.util import ngrams

MAX_NGRAMS_DEGREE = 3

code_states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

states_code={
     'Alaska':'AK'
    ,'Alabama':'AL'
    ,'Arkansas':'AR'
    ,'AmericanSamoa':'AS'
    ,'Arizona':'AZ'
    ,'California':'CA'
    ,'Colorado':'CO'
    ,'Connecticut':'CT'
    ,'DistrictofColumbia':'DC'
    ,'Delaware':'DE'
    ,'Florida':'FL'
    ,'Georgia':'GA'
    ,'Guam':'GU'
    ,'Hawaii':'HI'
    ,'Iowa':'IA'
    ,'Idaho':'ID'
    ,'Illinois':'IL'
    ,'Indiana':'IN'
    ,'Kansas':'KS'
    ,'Kentucky':'KY'
    ,'Louisiana':'LA'
    ,'Massachusetts':'MA'
    ,'Maryland':'MD'
    ,'Maine':'ME'
    ,'Michigan':'MI'
    ,'Minnesota':'MN'
    ,'Missouri':'MO'
    ,'NorthernMarianaIslands':'MP'
    ,'Mississippi':'MS'
    ,'Montana':'MT'
    ,'National':'NA'
    ,'NorthCarolina':'NC'
    ,'NorthDakota':'ND'
    ,'Nebraska':'NE'
    ,'NewHampshire':'NH'
    ,'NewJersey':'NJ'
    ,'NewMexico':'NM'
    ,'Nevada':'NV'
    ,'NewYork':'NY'
    ,'Ohio':'OH'
    ,'Oklahoma':'OK'
    ,'Oregon':'OR'
    ,'Pennsylvania':'PA'
    ,'PuertoRico':'PR'
    ,'RhodeIsland':'RI'
    ,'SouthCarolina':'SC'
    ,'SouthDakota':'SD'
    ,'Tennessee':'TN'
    ,'Texas':'TX'
    ,'Utah':'UT'
    ,'Virginia':'VA'
    ,'VirginIslands':'VI'
    ,'Vermont':'VT'
    ,'Washington':'WA'
    ,'Wisconsin':'WI'
    ,'WestVirginia':'WV'
    ,'Wyoming':'WY'
}
def sanitize_text(text):
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

def get_sentiment(tweet, scores):
    score = 0
    if tweet.has_key('text'):
        text = sanitize_text(tweet['text'])
        splitted_text = text.split()
        score_map = {}
        degree = range(min(len(splitted_text),MAX_NGRAMS_DEGREE) + 1, 0, -1)
        ignore_words = []
        for g in degree:
            ng = ngrams(splitted_text, g)
	    for words in ng:
	        term = ' '.join(words)
	        if scores.has_key(term):
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
    return score or 0

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

def get_location(tweet):

    location_grams = []
    if tweet.has_key('user') and tweet['user']:
        location = tweet['user'].get('location')
        if location:
            location_grams = location.split()
    elif tweet.has_key('place') and tweet['place']:
        place = tweet['place']
        if place.get('country_code').upper() == 'US':
            if place.get('place_type') == 'city':
                location_grams = place.get('full_name', '').split()
            else:
                location_grams = place.get('full_name')
    for gram in location_grams:
        if gram in code_states:
            return gram
        elif gram in states_code:
            return states_code[gram]
    else:
        return None

def main():
    try:
        sent_file = open(sys.argv[1])
        tweet_file = open(sys.argv[2])
        scores = parse_sentiment_file(sent_file)
        tweets = parse_tweets(tweet_file)
        states_scores = {}
        for tweet in tweets:
            loc = get_location(tweet)
            if loc:
                sentiment = get_sentiment(tweet, scores)
                if loc not in states_scores:
                    states_scores[loc] = {"sent" : sentiment, "counter" : 1}
                else:
                    states_scores[loc]["sent"] += sentiment
                    states_scores[loc]["counter"] += 1
        highest = None
        for key, value in states_scores.items():
            average = value["sent"]/( value["counter"] * 1.0)
            if not highest:
                highest = (key, average)
            elif highest[1] < average:
                highest = (key, average)
        print highest[0]
                    
    finally:
        sent_file.close()
        tweet_file.close()

if __name__ == '__main__':
    main()

