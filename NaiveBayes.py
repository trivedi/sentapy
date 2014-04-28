import math, nltk

from termcolor import colored

from analyze import generate_stopwords, sanitize
from vector import Vector

class NaiveBayesClassifier():

    def __init__(self):
        """
        Creates:

        """

        self.c = {"+" : Vector(), "-" : Vector()}
        for vector in self.c.values():
            vector.default = 1

        self.classes = ["+", "-"]
        self.prior = {"+" : 0.55, "-" : 0.45}
        self.stopwords = generate_stopwords()

        self.features = set()
        f = open("data/features_new.txt", "r")
        for line in f:
            self.features.add(line.strip().lower())
        f.close()

        # Begin training
        f_pos = open("data/train_pos.txt", "r")
        f_neg = open("data/train_neg.txt", "r")
        self.train("+", f_pos)
        self.train("-", f_neg)
        f_pos.close()
        f_neg.close()



    def train(self, sentiment, tweets):
        """

        @param {string} sentiment = "+" || "-"
               {iterable} tweets = file_with_tagged_tweets
        @return None
        """
        freq = self.c[sentiment]
        total = 0.0
        for tweet in tweets:
            total += 1
            words = sanitize(tweet, self.stopwords)
            for word in words:
                if word in self.features: # word in our pre-made features list
                    freq[word] += 100

        for word in freq:
            freq[word] = freq[word] / total

        freq.default = 1/total


    def posterior(self, sentiment, sanitized_tweet):
        """
        Computes the posterior (Bayesian Probability term) of a sanitized tweet

        Probability model for a classifier is a conditional model
        p(C, F1,...,Fn) = ( p(c)p(F1,...,Fn|C) ) / p(F1,...,Fn)

                        ...

        In English, using Bayesian Probability terminology, the equation can be written as

                     prior * likelihood
        posterior = --------------------
                        evidence

        in our case, we have:
            p(sentiment, sanitized_tweet)

        @param {string} sentiment = "+" or "-"
               {set} sanitized_tweet = set of sanitized words in tweet
        @return {float}
        """
        #print "sanitized tweet = %s" % sanitized_tweet
        #print math.log(self.prior[sentiment])
        #print "self.prior[sentiment] = %s" % self.prior[sentiment]
        p = math.log(self.prior[sentiment])

        

        values = self.c[sentiment]
        #print "%s : original p: %f" % (sentiment, p)


        for word in sanitized_tweet:
            if word in self.features: # word is in the features list, so apply the score for the feature based on the sentiment
                p += math.log(values[word])
          #      print "%s : %f" % (word, math.log(values[word]))
            else:
                p += math.log(.1 - values[word])
         #       print "%s : %f" % (word, math.log(.1 - values[word]))
        #print p
        return p


    '''
        for feature in self.features:
            #print "c[%s] = %s" % (feature, c[feature])
            if feature in sanitized_tweet:
                p += math.log(1 - c[feature]) # add feature's score per the sentiment
            else:
                p += math.log(1 - c[feature])
        return p
    '''       


    def classify(self, tweet, verbose=False, eval=False):
        """
        Classifies a text's sentiment given the posterior of of its class
        Picks the largest posterior between that of "+" and "-"

        However, if there is not enough confidence (i.e. if mpt posterior(c1|tweet) < 2*posterior(c2|tweet),
        then we classify as neutral ("~") because we don't have conclusive evidence

        @param {string} tweet
        @return {string} sentiment = "+" || "-" || "~"
        """


        sanitized = sanitize(tweet, self.stopwords)
       # print sanitized
        sentiment = {}
        for s in self.classes:
            sentiment[s] = self.posterior(s, sanitized) # Calculate posterior for positive and negative sentiment
        
        bigrams = nltk.bigrams(sanitized)
        for s in self.classes:
            for pair in bigrams:
             #   sentiment[s] += self.posterior(s, pair)
             #   if verbose: print (s, pair, self.posterior(s, pair))
             pass

        

        positive = sentiment["+"] # Get calculated posterior of positive sentiment
        negative = sentiment["-"] # Get calculated posterior fo negative sentiment

        #print "positive: %s negative: %s" % (positive, negative)
        '''
        if abs(positive - negative) < 1:
            return "~"
        elif positive > negative:
            return "+"
        else:
            return "-"
        '''
        if "not" in sanitized:
            if positive > negative:
                negative = abs(negative)
            elif negative > positive:
                positive = abs(positive)

        if verbose: print "positive: %f negative: %f" % (positive, negative)
        if positive > + math.log(2) + negative:
            if eval: return "+"
            else: print colored('+', 'green')
        elif negative > math.log(1)+positive:
            if eval: return "-"
            else: print colored('-', 'red')
        else:
            if eval: return "~"
            else: print colored('~', 'white')

    def evaluate(self):
        t = w = 0 # total = 0, wrong = 0
        missed_pos = []
        for tweet in open("data/verify_pos.txt"):
            t += 1.0
            if "+" != self.classify(tweet, False, eval=True):
                missed_pos += [(tweet.strip(), self.classify(tweet))]
                w += 1.0
        print "Positive - accuracy: %s" % self.accuracy(w, t) # make function that displays values correctly
        #print "Missed positives:"
      #  for tweet in missed_pos:
       #     print tweet
        
        t = w = 0
        for tweet in open("data/verify_neg.txt"):
            t += 1.0
            if "-" != self.classify(tweet, False, eval=True):
                w += 1.0
        print "Negative - accuracy: %s" % self.accuracy(w, t)

        w = t = 0
        for tweet in open("data/verify_neutral.txt"):
            t += 1.0
            if "~" != self.classify(tweet, verbose=False, eval=True):
                w += 1.0
        print "Neutral - accuracy: %s" % self.accuracy(w, t)




    def accuracy(self, w, t):
        return str( (1 - (w/t)) * 100 )


    def __repr__(self):
        pass




c = NaiveBayesClassifier()
c.evaluate()
