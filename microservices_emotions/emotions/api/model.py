import os
import pickle
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model


class Emotions(object):
    def __init__(self, path):
        self.path = path
        self.model = None
        self.id2label = None
        self.tokenizer = None

    def load_model(self):
        # Load pretrained model
        self.model = load_model(os.path.join(self.path, "model_att_v1.h5"))
        # Load tokenizer.
        path = os.path.join(self.path, 'tokenizer.pickle')
        print(path)
        with open(path, 'rb') as handle:
            self.tokenizer = pickle.load(handle)
        # Load id2label dictionary.
        path = os.path.join(self.path, 'id2label.pickle')
        print(path)
        with open(path, 'rb') as handle:
            self.id2label = pickle.load(handle)

    def get_emotion(self, text):
        max_length = 178
        trunc_type = "post"
        sequences = self.tokenizer.texts_to_sequences([text])

        padded = pad_sequences(
            sequences,
            maxlen=max_length,
            padding=trunc_type,
            truncating=trunc_type
        )

        return self.id2label[np.argmax(self.model.predict(padded))]
