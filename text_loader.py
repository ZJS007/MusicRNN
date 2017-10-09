import numpy as np
from parameters import model_params


class TextLoader():
    def __init__(self, file_, batch_size, seq_size):
        self.batch_size = batch_size
        self.seq_size = seq_size
        self.all_data = open('data/%s' % file_).read()
        self.create_batches()
        self.reset_batch_pointer()

    def create_batches(self):
        self.n_batches = int(len(self.all_data) / (self.batch_size *
                                                     self.seq_size))
        data = list(self.all_data[:self.n_batches * self.batch_size *
                                  self.seq_size])
        data = np.array([model_params.char_to_key[char] for char in data])
        target = np.array([None for _ in data])
        target[:-1] = data[1:]
        target[-1] = data[0]
        self.data = np.split(data.reshape(self.batch_size, -1),
                             self.n_batches, 1)
        self.target = np.split(target.reshape(self.batch_size, -1),
                               self.n_batches, 1)

    def get_next_batch(self):
        data, target = self.data[self.pointer], self.target[self.pointer]
        self.pointer += 1
        return data, target

    def reset_batch_pointer(self):
        self.pointer = 0