import string
import numpy as np
import pickle
import argparse


class Train:

    def __init__(self, data):
        self.data = data

    def norma(self):
        #очистка текста
        words = np.array("".join(c.lower() for c in self.data if (c.isalpha() | (c == ' '))).split(' '))
        return words

    def fit(self, data):
        model = {}
        unique = np.unique(data)
        #создание пустого словаря
        for u in unique:
            model[u] = []
        for u in unique:
            #создание массива контекстных слов
            act_word, = np.where(data == u)
            next_word = np.array([data[a + 1] for a in act_word if a != len(data) - 1])
            #создание массива уникальных значений контекстых слов и их подсчет
            unique_cont, counts = np.unique(next_word, return_counts=True)
            #заполнение словаря контекстными словами и вероятностями
            for val, coun in zip(unique_cont, counts):
                model[u].append([val, coun / np.sum(counts)])
        return model

    def generate(self, model, url):
        #сохранение модели в файл
        with open(url, 'wb') as f:
            pickle.dump(model, f)

#создание консольного парсера        
parser = argparse.ArgumentParser()
#добавление аргументов в парсер
parser.add_argument('--input-dir', dest='input_dir',
type = str)
parser.add_argument('--model', type=str)
args = parser.parse_args()
#открытие файла с датасетом
f = open(args.input_dir, 'r')
data = f.read().replace('\n', ' ')
#создание объекта класса Train
model = Train(data=data)
#нормализация текста, обучение модели и сохранение файла
norm_text = model.norma()
fit_model = model.fit(norm_text)
model.generate(fit_model, args.model)
