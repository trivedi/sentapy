import math, re
from vector import Vector

def generate_stopwords():
    """
    return set because membership access is much faster than using lists (lists are faster at iterating

    @return {set}
    """
    stopwords = set()

    f = open("data/stopwords.txt")
    for line in f.readlines():
        stopwords.add( line.strip("\n") )
    f.close()
    return stopwords


def sanitize(text, stopwords):
    """
    Cleanup text to get rid of usless words and symbols
    1) @usernames
    2) RT (retweets)
    3) #Hashtags
    4) URLs
    5) Stopwords
    6) Punctuation (besides smiley face)

    @param {string} tweet
           {set} stopwords
    @return {set}
    """

    text = text.lower()
    words = text.split()
    words = [word for word in words if "@" not in word] # remove @usernames
    words = [word for word in words if "rt" not in word] # remove retweets
    #words = [word for word in words if "#" not in word] # remove #hashtags
    words = [word.replace('#', '') for word in words]
    words = [word for word in words if not word.startswith("http")] # remove URLs


    # Experimental

    text = " ".join(words)


    slang = {
            "lol":"laughing out loud",
             "lmao":"laughing",
             "rofl":"laughing",
             "omg":"oh my god",
             "idk":"i don't know",
             "fav":"favorite",
             "fave":"favorite"
            }

    # replace abbreviations with their actual meaning
    # "lol" -> "laughing out loud"
    # "omg" -> "oh my god"
    for word in words:
        if word in slang:
            text = text.replace(word, slang[word])

    words = text.split()
    words = [word for word in words if word not in stopwords] # remove stopwords again if they were added in
    words = [word for word in words if not word.isdigit()] # remove numbers (only works for integers)

### END OF EXPERIMENTAL ###

    text = " ".join(words)
    words = re.findall("\w+", text)
    words.extend(re.findall("['\-/()=:;]['\-/()=:;]+", text))
    words = {word for word in words if len(word) > 1 and word.lower() != "rt"}

    words = {word for word in words if word not in stopwords} # remove stopwords


    return words


def probability(vector, x, t):
    """
    Finds the probability of vector[x] in t occurnences
    If x is not in vector then the probability is .001/t

    @param {Vector} vector
           {int} x
           {float} t
    @return {float}
    """
    t = t*1.0
    return vector[x] / t or 0.001 / t

def binary_entropy(p):
    """
    Uses the binary entropy function denoted H(p) in information theory/statistics
    Computes the entropy of a Bernoulli process with probability of success p

    When p = .5, entropy is at its max value (unbiased bit, most common unit of information entropy)

    @param {float} p = probability of success p
    @return {float}
    """
    return -p * math.log(p,2) - (1 - p) * math.log(1-p, 2)


def features():
    """
    Called with -features flag
    Prints top 100 words with the highest information gain

    Need to keep a {Vector} both that tracks positive and negative words because some words are ambiguous or neutral (stopwords that were not filtered)

    @return None
    """

    positives = Vector() # Contains word-freq pairs for positive words
    negatives = Vector() # Contains word-freq pairs for negative words
    both = Vector() # Contains word-freq pairs for all words

    p = n = words = 0 # keeps track of occurences of positive, negative, and total words
    stopwords = generate_stopwords()

    f = open("data/train_pos.txt", "r")
    for tweet in f:
        for word in sanitize(tweet, stopwords): # sanitize tweets to get rid of unecessary information that could confuse/corrupt  classification
            positives[word] += 1
            both[word] += 1
            p += 1
            words += 1
    f.close()

    # repeat above process on negative tweets
    f = open("data/train_neg.txt", "r")
    for tweet in f:
        for word in sanitize(tweet, stopwords):
            negatives[word] += 1
            both[word] += 1
            n += 1
            words += 1
    f.close()

    features = []
    for word in both:
        p_both = probability(both, word, words) # find probability of a word that appears in positive and negative Vectors
        p_pos = probability(positives, word, p) # find probability that word is positive.
        p_neg = probability(negatives, word, n) # find probability that word is negative.

        h = binary_entropy(p_both) - ( p/words * binary_entropy(p_pos) ) - ( n/words * binary_entropy(p_neg) )

        features.append( (word, h) )

    for word in [word for word in sorted(features, key=lambda x: -x[1])[:100]]:
        if word[0] in positives:
            print "entropy(%s, positive) = %s" % (word[0], word[1])
        else:
            print "entropy(%s, negative) = %s" % (word[0], word[1])
        
