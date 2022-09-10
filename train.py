import string
import numpy as np
import pickle
import argparse


class Train:

    def __init__(self, data):
        self.data = data

    def norma(self):
        words = "".join(c for c in self.data if (c.isalpha() | (c == ' ')))
        words = np.array([w.translate(str.maketrans('', '', string.punctuation)).replace('\n', '') for w in
                          words.lower().split(' ')])
        return words

    def fit(self, data):
        model = {}
        unique = np.unique(data)
        for u in unique:
            model[u] = []
        for u in unique:
            act_word, = np.where(data == u)
            next_word = np.array([data[a + 1] for a in act_word if a != len(data) - 1])
            unique_cont, counts = np.unique(next_word, return_counts=True)

            for val, coun in zip(unique_cont, counts):
                model[u].append([val, coun / np.sum(counts)])
        return model

    def generate(self, model, url):
        with open(url, 'wb') as f:
            pickle.dump(model, f)

        
parser = argparse.ArgumentParser()
parser.add_argument('--input-dir', dest='input_dir',
type = str)
parser.add_argument('--model', type=str)
args = parser.parse_args()
f = open(args.input_dir, 'r')
data = f.read()
model = Train(data=data)
norm_text = model.norma()
fit_model = model.fit(norm_text)
model.generate(fit_model, args.model)
