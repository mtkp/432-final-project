#!/usr/bin/python2.7

import random

WORDS_FILE      = "min_8"

# returns list of ten words chosen randomly form larger list
def get_random_words(all_words):
    real_word_list = []
    range_max = len(all_words) - 1
    for _ in xrange(500):
        real_word_list.append(all_words[random.randint(0, range_max)])
    return real_word_list

# opens text file and rturns a small list of the words
def read_words(words_file=WORDS_FILE):
    all_words = [word for line in open(words_file, 'r') for word in line.split()]
    return get_random_words(all_words)


if __name__ == "__main__":
    for word in read_words():
        print word