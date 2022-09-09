import pickle
import numpy as np
import random
import argparse


class Generate:

    def __init__(self, length):
        self.length = length

    def sentence(self, model):
        first_word = random.choice(list(model))
        sentence = [first_word]
        for i in range(self.length - 1):
            temp_val = fit_model[first_word]
            temp_prob = []
            for i in range(len(temp_val)):
                temp_prob.append(temp_val[i][1])
            while len(temp_val) > 2:
                temp_val.pop(temp_prob.index(min(temp_prob)))
                temp_prob.pop(temp_prob.index(min(temp_prob)))
            first_word = random.choice(list(temp_val))[0]
            sentence.append(first_word)
        return ' '.join(sentence).capitalize()

    def load(self, model):
        with open(model, 'rb') as f:
            fit_model = pickle.load(f)
        return fit_model

parser = argparse.ArgumentParser()
parser.add_argument('--length', type=int)
parser.add_argument('--model', type=str)
args = parser.parse_args()
model = args.model
generator = Generate(args.length)
fit_model = generator.load(model)
sentence = generator.sentence(fit_model)
print(sentence)
