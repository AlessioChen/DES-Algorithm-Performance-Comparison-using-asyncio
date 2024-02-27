import random 
import string 
import os 


def generate_words(N, length):

    char_set = string.ascii_letters + string.digits + './'
    words = []
    for _ in range(N):
        w = ''.join( random.choice(char_set) for _ in range(length))
        words.append(w)

    return words

words = generate_words(100000, 8)

with open("words.txt", "w") as f:
    for word in words: 
        f.write(word + "\n")
