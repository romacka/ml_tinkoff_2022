import string
import re
import sys
import numpy as np
import pickle
import argparse




class Train:

    def __init__(self, data):
        self.data = data
    def norma(self):
        self.data = "".join(c for c in self.data if ((c.isalpha()) | (c == " ")))
        self.data = self.data.lower()
        words = self.data.split(' ')
        for word in words:
            if word == '':
                words.remove(word)
        return words
    
    def fit(self, data):
        matr = np.zeros((len(set(data)), len(set(data))))
        unique = list(set(data))

        for i in range(len(data)):
            for j in range (len(data)-2):
                if data[i] == data[j]:
                    matr[unique.index(data[i])][unique.index(data[j+1])] = matr[unique.index(data[i])][unique.index(data[j+1])] + 1
        model = {}

        for l in range(len(unique) - 1):
            pair_emb_count = 0
            pair_context_count = 0
            last_context = []
            for m in range(len(unique) - 1):
                if matr[l][m] != 0:
                    pair_emb_count = pair_emb_count + matr[l][m]
                    
            for n in range(len(unique) - 1):
                if matr[l][n] != 0:
                    for k in range(len(unique) - 1):
                        if matr[k][n] != 0:
                            pair_context_count = pair_context_count + matr[k][n]
                    prob = matr[l][n] * matr[l][n] / pair_emb_count / pair_context_count


                    last_context.append((unique[n], prob))
                    model[unique[l]] = last_context
        return model


    def generate(self, model, output):
        with open(output, 'wb') as f:
            pickle.dump(model, f)


        return 0


parser = argparse.ArgumentParser()
parser.add_argument('--input-dir',dest='input_dir', type=str, help='Input dir for videos')
parser.add_argument('--model', type=str, help='Output dir for image')
args = parser.parse_args()

f = open(args.input_dir, 'r')
data = f.read()
model = Train(data=data)
norm_text = model.norma()

fit_model = model.fit(norm_text)
model.generate(fit_model, args.model)
