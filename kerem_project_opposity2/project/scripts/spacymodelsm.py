# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 21:31:21 2020

@author: Kerem's Laptop
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 20:21:14 2020

@author: Kerem's Laptop
"""
import spacy
import praw  # for Reddit threads
import pandas as pd  # for data science
from psaw import PushshiftAPI  # for Reddit comments
import twint  # for tweets
import nest_asyncio
import re
import nltk
from nltk.stem import WordNetLemmatizer
import asyncio
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
https = urllib3.PoolManager()


def spacysmscraper(text, number):
    # print("1")
    asyncio.set_event_loop(None)  # Clear the main loop.
    loop = asyncio.new_event_loop()  # Create a new loop.
    nest_asyncio.apply(loop)
    # print("2")
    # Part 1: for Reddit threads
    reddit = praw.Reddit(client_id='7hU5ZrX236KkyQ',
                         client_secret='c6pSBGl5Z2O1nwc-j-iuFhwGwfs',
                         redirect_uri='http://localhost:8080',
                         user_agent='trialnewbyopposity'
                         )
    all = reddit.subreddit("technology+tech+futurology+engineering+army+navy+airforce+geek+military+scifi+science")
    topics_dict = {"Text": [], "Date": [], "Score": [], "Upvote_Ratio": []}
    for submission in all.search(text, limit=number):
        topics_dict["Text"].append(submission.title)
        topics_dict["Date"].append(submission.created_utc)
        topics_dict["Score"].append(submission.score)
        topics_dict["Upvote_Ratio"].append(submission.upvote_ratio)
    topics_data = pd.DataFrame(topics_dict)
    topics_data['Date'] = (pd.to_datetime(topics_data['Date'], unit='s'))
    listeforlabel = ['Reddit Thread'] * number
    dflisteforlabel = pd.Series(listeforlabel)
    upnewdf = pd.concat([topics_data, dflisteforlabel], axis=1)

    # Part 2: for Reddit comments
    subbies = ["technology", "tech", "futurology", "engineering", "army", "navy", "airforce", "geek", "military",
               "scifi", "science"]
    api = PushshiftAPI()
    gen = api.search_comments(q=text, subreddit=subbies)
    cache = []
    for c in gen:
        cache.append(c)
        if len(cache) >= number:
            break
    comments_dict = {"Text": [], "Date": []}
    for x in cache:
        comments_dict["Text"].append(str(x[14]))
        comments_dict["Date"].append(x[16])
    commentdf = pd.DataFrame(comments_dict)
    commentdf['Date'] = (pd.to_datetime(commentdf['Date'], unit='s', errors="coerce"))
    listforlabel = ['Reddit Comment'] * number
    dflistforlabel = pd.Series(listforlabel)
    newdf = pd.concat([commentdf, dflistforlabel], axis=1)

    # Part 3: for Tweets
    c = twint.Config()
    c.Search = text
    c.Limit = number
    c.Pandas = True
    # c.Since
    # c.Until
    twint.run.Search(c)
    Tweets_df = twint.storage.panda.Tweets_df
    necessary_text = Tweets_df.tweet
    necessary_date = Tweets_df.date
    necessary_likes = Tweets_df.nlikes
    necessary_retweets = Tweets_df.nretweets
    tweetlabel = ['Tweet'] * len(necessary_text)
    tweforlabel = pd.Series(tweetlabel)
    lastlabel = pd.concat([necessary_text, necessary_date], axis=1)
    finallabel = pd.concat([lastlabel, tweforlabel], axis=1)
    finallabel.rename(columns={"tweet": "Text", "date": "Date"}, inplace=True)
    final2label = pd.concat([finallabel, necessary_likes], axis=1)
    final3label = pd.concat([final2label, necessary_retweets], axis=1)

    # Combine Part 1, Part 2, Part 3
    frames = [upnewdf, newdf, final3label]
    result = pd.concat(frames)
    result.columns = ["Date", "Score", "Text", "Upvote Ratio", "Type", "Likes", "Retweets"]
    # Specify symbols to keep in text
    symbols_to_keep = "1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM:;!-,?.@ \n\"\'"

    # Function for removing unknown characters
    remove_unknown_chars = lambda x: ''.join(char for char in x if char in symbols_to_keep)
    # Function for removing all Twitter user tags (@ongunuzaymacar, etc.)
    remove_user_tags = lambda x: re.sub(r'@\w+', '', x)
    # Function for removing all Twitter hashtags (#freetheworld, ect.)
    remove_hash_tags = lambda x: re.sub(r'#\w+', '', x)
    # Function for removing all URLs (www.google.com, etc.)
    remove_urls = lambda x: re.sub(r'(https://|www.)[A-Za-z0-9_.]+', '', x)

    def clean_tweets(twoot):
        # Convert to lowercase and remove spaces from beginning
        twoot = str(twoot).lstrip()
        # Remove Twitter-related data
        twoot = remove_user_tags(twoot)
        twoot = remove_urls(twoot)
        twoot = remove_hash_tags(twoot)
        # Remove unwanted characters
        twoot = remove_unknown_chars(twoot)
        # Remove spaces from end and condense multiple spaces into one
        twoot = twoot.rstrip()
        twoot = re.sub(' +', ' ', twoot)
        return twoot

    result["Text"] = result["Text"].apply(clean_tweets)
    f = lambda x: " ".join(x["Text"].split())
    result["Text"] = result.apply(f, axis=1)

    def ner(x):
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(x)
        textually = []
        tags = []
        for ent in doc.ents:
            textually.append(ent.text)
            tags.append(ent.label_)
        spacy_dictionary = dict(zip(textually, tags))
        good_terms = []
        for key in spacy_dictionary:
            if spacy_dictionary[key] == "ORG":
                good_terms.append(key)
            if spacy_dictionary[key] == "GPE":
                good_terms.append(key)
            if spacy_dictionary[key] == "LOC":
                good_terms.append(key)
            if spacy_dictionary[key] == "PRODUCT":
                good_terms.append(key)
            if spacy_dictionary[key] == "DATE":
                good_terms.append(key)
            if ("PRODUCT" not in spacy_dictionary.values()) and ("ORG" not in spacy_dictionary.values()):
                good_terms.clear()
            return good_terms

    result["NER Model"] = result["Text"].apply(ner)
    return result

# example = spacysmscraper("science", 1)
# print(example)
# example.to_csv("spacymodelsm.csv", index=False)
