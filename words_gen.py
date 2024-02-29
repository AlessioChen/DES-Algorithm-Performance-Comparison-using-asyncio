import random
import string
import os
import des
import json


def generate_words(N, length):
    char_set = string.ascii_letters + string.digits + './'
    words = {}
    for _ in range(N):
        w = ''.join(random.choice(char_set) for _ in range(length))
        words[w] = des.encrypt(w)

    return words


words = generate_words(10000, 8)

json_object = json.dumps(words, indent=4)
with open("words.json", "w") as f:
    f.write(json_object)
