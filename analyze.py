import nltk, numpy, re, sys
#from vector import Vector

def generate_stopwords():
    """
    return set because membership access is much faster than using lists (lists are faster at iterating

    @return set
    """
    stopwords = nltk.corpus.stopwords.words("english")
    return set(stopwords)


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
    words = [word for word in words if "#" not in word] # remove #hashtags
    words = [word for word in words if not word.startswith("http")] # remove URLs
    words = [word for word in words if word not in stopwords] # remove stopwords

    text = " ".join(words)

    # Experimental

    slang = {
            "lol":"laughing out loud",
             "lmao":"laughing my ass off",
             "rofl":"rolling on the floor laughing",
             "omg":"oh my god",
             "idk":"i don't know",
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

    return set(words)





# Tests
assert generate_stopwords() == set(nltk.corpus.stopwords.words("english"))
print sanitize("RT @nishadtrivedi omg I have 2 weeks to complete this project! lmao", generate_stopwords())
#assert sanitize("RT @nishadtrivedi I have 2 weeks to complete this project! lmao", generate_stopwords()) == {"weeks", "complete", "project"}
