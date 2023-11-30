"""
Loop through donald's tweet and make a markov chain out of it
"""
import sys
import pandas as pd
from nltk.tokenize import RegexpTokenizer
import re
from scipy.sparse import dok_matrix
from itertools import chain
import numpy as np
from scipy.sparse import csr_matrix
from numpy.random import choice
from tqdm import tqdm
import pickle
import concurrent.futures



def split_regex_word(word):
    regex_match = re.match(r'^([^a-zA-Z0-9]*)(.*?)([^a-zA-Z0-9]*)$', word)
    if regex_match:
        prefix, main, suffix = regex_match.groups()
        return prefix, main, suffix
    else:
        return '', word, ''



def clean_text(text):
    """
    Remove hyperlinks and quotation marks
    concat all tweet into one giant text
    """
    processed_tweets = []
    tokenizer = RegexpTokenizer('\w+|\S+')
    for tweet in text:
        tweet = re.sub('(https?:[\w\/\.\d]+)|…|(^RT)|“|”|"', "", tweet)
        tweet = re.sub("&amp;?", "and", tweet)
        processed_tweets.append(tokenizer.tokenize(tweet.lower()))

    gigantic_text = []
    for tweet in processed_tweets:
        for word in tweet:
            word=word.strip()
            pref, w, suf = split_regex_word(word)
            if pref!='':
                gigantic_text.append(pref)
            if w!='':
                gigantic_text.append(w)
            if suf!='':
                gigantic_text.append(suf)
#            if word=='' or word==' ':
#                pass
#            if word[-1] in [".", "!", "?", ")", "'", "\""]:
#                if word[:-1]!='':
#                    gigantic_text.append(word[:-1])
#                gigantic_text.append(word[-1])
#            elif word[0] in ["(", "'", "\""]:
#                if word[1:]!='':
#                    gigantic_text.append(word[1:])
#                gigantic_text.append(word[0])
#            else:
#                gigantic_text.append(word)
    breakpoint()
    return gigantic_text


def dict_of_next_word(curr_word, data):
    """
    go through data, get list of next word after curr_word, count them
    return dictionary
    """
    indices = [index for index, word in enumerate(data) if word == curr_word]
    if len(data)-1 in indices:
        indices.remove(len(data)-1)

    next_words = [data[i+1] for i in indices]

    return {item: next_words.count(item) for item in set(next_words)}




def markovify(data):
    """
    make a markov chain out of it, dictionary form

    markovD[word]=word_dict
        with
        word_dict[next_word]=occurence
    """
    markovD = {}
    distinct_words = list(set(data))

    def process_word(word):
        print(word)
        markovD[word] = dict_of_next_word(word, data)

    # parallelize! So it doesn't take forever
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
        # Use tqdm to display a progress bar
        for _ in tqdm(executor.map(process_word, distinct_words), total=len(distinct_words)):
            pass

    return markovD

if __name__=="__main__":
    data0 = pd.read_csv(str(sys.argv[1]))
    data1 = pd.read_csv(str(sys.argv[2]))
    data = pd.concat([data0['Tweet Text'], data1['Tweet Text']], axis=0).to_list()
    cleaned = clean_text(data)
    markoved = markovify(cleaned)
    print("saving!")
    #saving the markov chain into pickle file
    with open('markov_chain.pkl', 'wb') as f:
        pickle.dump(markoved, f)
