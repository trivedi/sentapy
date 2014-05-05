#!/usr/bin/env python

from __future__ import print_function
import twitter, analyze, os
from NaiveBayes import c
from termcolor import colored



def menu():

    global flag
    flag = False
    
    os.system("clear")
    print(colored("Sentapy - {Sentiment Analysis in Python}", "blue"))
    print()
    while True:
        print(colored('{menu} > ', 'yellow'), end="") 
        input = raw_input().lower()
        if input == "classify":
            classify(flag)
        elif input == "verbose":
            flag = verbose(flag)
        elif input == "evaluate":
            evaluate()
        elif input == "twitter":
            query()
        elif input == "features":
            features()
        elif input in ["exit", "quit", "q"]:
            exit()
        elif input == "clear":
            os.system('clear')
        else:
            help()


def help():
        print("Choices:")
        print("classify\n\tClassify sentence")
        print("twitter\n\tStream tweets and find find sentiment")
        print("features\n\tFind top 100 feature-words with the most information gain")
        print("evaluate\n\tFind accuracy of classifier on manually analyzed tweets")
        print("verbose\n\tToggle flag, prints extra information")

def classify(flag):
    while True:
        print(colored('{classify} > ', 'yellow'), end="") 
        i = raw_input()
        if i in ["exit", "quit", "q", "back"]:
            break
        elif i == "clear":
            os.system('clear')
        else:
            c.classify(i, verbose=flag)

def evaluate():
    c.evaluate()

def query():
    twitter.run()

def features():
    analyze.features()

def verbose(flag):
    flag = not flag
    if flag:
        print("Verbosity is " + colored("[on]", "green"))
        return flag
    else:
        print("Verbosity is " + colored("[off]", "red"))
        return flag



if __name__ == '__main__':
    menu()
