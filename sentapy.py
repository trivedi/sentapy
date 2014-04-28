import NaiveBayes, twitter, analyze
from NaiveBayes import c

def menu():

    global flag
    flag = False

    print "Sentapy - {Sentiment Analysis in Python}"
    while True:
        input = raw_input("{menu} > ").lower()

        if input == "classify":
            classify(flag)
        elif input == "verbose":
            flag = verbose(flag)
        elif input == "evaluate":
            evaluate()
        elif input == "twitter":
            query()
        elif input in ["exit", "quit", "q"]:
            exit()
        else:
            help()


def help():
        print "Choices:"
        print "classify\n\tClassify sentence"
        print "twitter\n\tStream tweets and find find sentiment"
        print "features\n\tFind top 100 feature-words with the most information gain"
        print "evaluate\n\tFind accuracy of classifier on manually analyzed tweets"
        print "verbose\n\tToggle flag, prints extra information"

def classify(flag):
    while True:
        i = raw_input("{classify} > ")
        if i in ["exit", "quit", "q", "back"]:
            break
        c.classify(i, verbose=flag)


def evaluate():
    c.evaluate()


def query():
    twitter.run()

def verbose(flag):
    flag = not flag
    if flag:
        print "Verbosity is [on]"
        return flag
    else:
        print "Verbosity is [off]"
        return flag



if __name__ == '__main__':
    menu()
