"""
given a markov chain, start tweeting!
"""
import pickle
import random

def get_next_word(curr_word, choices):
    if curr_word=="@" or curr_word=="the" or curr_word=="and":
        return random.choice(list(choices.keys()))


    # randomize? yes if 1 else no
    if len(choices)==1:
        return list(choices.keys())[0]

    if random.random()<0.1: # chances of randomization 20%
        next_word = random.choice(list(choices.keys()))
    else: # not randomize
        next_word = max(choices, key=choices.get)

    if next_word=="@" or next_word=="great":
        return random.choice(list(choices.keys())) if random.random()>0.5 else next_word
    return next_word


def tweet(markov):
    # get random first word
    curr_word = random.choice(list(markov.keys()))
    #tweet = [get_next_word(curr_word, markov[curr_word])]
    tweet = [curr_word]
    # loop till encounter '.', '?', '!' or word limit hit 300
    while True:
        if tweet[-1] in [".", "?", "!"] or len(tweet)>1000:
            if len(tweet)>2:
                return " ".join(tweet)
            else:
                tweet.append(get_next_word(tweet[-1], markov[tweet[-1]]))
        else:
            tweet.append(get_next_word(tweet[-1], markov[tweet[-1]]))



def tweet_starting(curr_word, markov):
    #tweet = [curr_word, get_next_word(curr_word, markov[curr_word])]
    tweet = [curr_word]
    # loop till encounter '.', '?', '!' or word limit hit 300
    while True:
        if tweet[-1] in [".", "?", "!"] or len(tweet)>1000:
            if len(tweet)>5:
                return " ".join(tweet)
            else:
                tweet.append(get_next_word(tweet[-1], markov[tweet[-1]]))
        else:
            tweet.append(get_next_word(tweet[-1], markov[tweet[-1]]))


if __name__=="__main__":
    with open('markov_chain.pkl', 'rb') as f:
        markov = pickle.load(f)

    print(tweet_starting('biden', markov))
    print()

    # tweet 50 tweets!
    #for _ in range(10):
    #    print(tweet(markov))
    #    print("-----------------------------------")
