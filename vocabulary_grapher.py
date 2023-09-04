# Loading data
import json
import numpy as np
import urllib.request
from gensim.models import KeyedVectors
import os
import tensorflow as tf
from tensorboard.plugins import projector

model = KeyedVectors.load_word2vec_format('/content/drive/MyDrive/Colab Notebooks/GoogleNews-vectors-negative300.bin.gz', binary=True)

def load_words():
    with urllib.request.urlopen('https://raw.githubusercontent.com/dwyl/english-words/master/words_dictionary.json') as file:
        words = json.loads(file.read().decode())

    return words

dict_words = load_words()
# dict_words

# Initialise centre and axis words
centre_word = "happy"
axis_words = ["formal", "enthusiastic", "mellow"]

# ERROR HANDLING: Are the centre/axis words in the model?

n = len(axis_words)
centre_word_pos = {centre_word: np.zeros(n, dtype=int)}
axis_word_pos = {}
for i in range(n):
  v = np.zeros(n)
  axis_word_pos[axis_words[i]] = v

centre_word_pos
axis_word_pos

# Similarity of centre word with each axis word to compute axis word positions.
for i in range(n):
  aw = axis_words[i]
  axis_word_pos[aw][i] = 1 - model.similarity(aw, centre_word) # Higher similarity means closer to origin
axis_word_pos

outliers = []
for dict_word in dict_words.keys():
  if dict_word not in model:
    outliers.append(dict_word)
for dict_word in outliers:
  del dict_words[dict_word]

len(dict_words)

# Similarity of centre word with each dictionary word to determine whether it is
# added to the word cloud.
threshold = 0.5
graph_word_pos = {}
for dict_word in dict_words.keys():
  if model.similarity(dict_word, centre_word) > threshold:
    v = np.zeros(n)
    graph_word_pos[dict_word] = v

graph_word_pos

# Similarity of each axis word with each graph word to determine the graph word's
# position in the cloud.
# Compute similarity in M dimensional space, then use PCA to reduce to 3d

for graph_word in graph_word_pos.keys():
  for i in range(n):
    aw = axis_words[i]
    val = model.similarity(graph_word, aw)
    graph_word_pos[graph_word] += val * axis_word_pos[aw]

graph_word_pos[centre_word] = centre_word_pos[centre_word]
graph_word_pos.update(axis_word_pos)

graph_word_pos

# Commented out IPython magic to ensure Python compatibility.
try:
  # %tensorflow_version only exists in Colab.
#   %tensorflow_version 2.x
except Exception:
  pass

# %load_ext tensorboard

log_dir='/logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

with open(os.path.join(log_dir, 'metadata.tsv'), "w") as f:
  for dict_word in graph_word_pos.keys():
    f.write("{}\n".format(dict_word))

weights = tf.Variable(tf.convert_to_tensor(list(graph_word_pos.values())))
weights

checkpoint = tf.train.Checkpoint(embedding=weights)
checkpoint.save(os.path.join(log_dir, "embedding.ckpt"))

# Set up config.
config = projector.ProjectorConfig()
embedding = config.embeddings.add()
# The name of the tensor will be suffixed by `/.ATTRIBUTES/VARIABLE_VALUE`.
embedding.tensor_name = "embedding/.ATTRIBUTES/VARIABLE_VALUE"
embedding.metadata_path = 'metadata.tsv'
projector.visualize_embeddings(log_dir, config)

# Commented out IPython magic to ensure Python compatibility.
# Now run tensorboard against on log data we just saved.
# %load_ext tensorboard
# %tensorboard --logdir /logs

#%reload_ext tensorboardi