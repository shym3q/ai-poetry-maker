import numpy as np
import tensorflow as tf
import keras
from keras.preprocessing.text import Tokenizer
from keras_preprocessing.sequence import pad_sequences 
import pickle
from math import floor


class Poet():
    def __init__(self, name: str, seed: str):
        self.name = name
        self.seed = seed
        self.model = keras.models.load_model(f'models/{self.name} model.h5')
        self.max_sequence_len = self.model.get_config()['layers'][0]['config']['batch_input_shape'][1] + 1
        with open(f'tokenizers/{self.name} tokenizer.pickle', 'rb') as handle:
            self.tokenizer = pickle.load(handle)
    
    def generate(self):
        line_len = len(self.seed.split())
        words = floor(100/line_len) * line_len + line_len
        for _ in range(words):
            token_list = self.tokenizer.texts_to_sequences([self.seed])[0]
            token_list = pad_sequences([token_list], maxlen=self.max_sequence_len-1, padding='pre')
            predicted = np.argmax(self.model.predict(token_list), axis=-1)
            output_word = ''
            for word, index in self.tokenizer.word_index.items():
                if index == predicted:
                    output_word = word
                    break
            self.seed += ' ' + output_word
        return self.merge(line_len)
    
    def merge(self, line_len: int):
        line = ''
        poem = ''
        for idx, word in enumerate(self.seed.split()):
            line += word + ' '
            if (idx + 1) % line_len == 0:
                poem += line + '\n'
                line = ''
        return poem
