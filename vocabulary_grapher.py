# Loading data
import json, urllib.request

def load_words():
    with urllib.request.urlopen('https://raw.githubusercontent.com/dwyl/english-words/master/words_dictionary.json') as file:
        words = json.loads(file.read().decode())

    return words

dict_words = load_words()
# dict_words

centre_word = "happy"
axis_words = ["formal", "enthusiastic", "mellow"]

n = len(axis_words)
axis_word_pos = {}
for i in range(n):
  v = [0 for j in range(n)]
  v[i] = 1
  axis_word_pos[axis_words[i]] = v

#axis_word_pos

