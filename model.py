import os
import tensorflow as tf
import tensorflow.contrib as tfcontrib
import numpy as np
from parameters import model_params, sample_params
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


# MAINLY BASED ON CHAR-RNN https://github.com/karpathy/char-rnn
# and https://github.com/sherjilozair/char-rnn-tensorflow
# and other tensorflow tutorials ..

class Model():

    def __init__(self, model_params, in_training=True):
        # Get params
        self.params = model_params

        # If we are not in training, we'll use only one character to sample
        # (no batch, no seq) + no dropout when we sample
        if not in_training:
            self.params.batch_size = 1
            self.params.seq_size = 1
            self.params.output_keep_prob = 1

        # These are our neurons, LSTM (Long short term memory) wich are more
        # complex than normal formal neurons (see
        # http://colah.github.io/posts/2015-08-Understanding-LSTMs/
        # for more info on LSTMs).
        # We have 'n_layer' layer of 'layer_size' neurons
        cells = [tfcontrib.rnn.DropoutWrapper(
                    tfcontrib.rnn.BasicLSTMCell(self.params.layer_size),
                    output_keep_prob=self.params.output_keep_prob)
                 for _ in range(self.params.n_layer)]
        self.cell = tfcontrib.rnn.MultiRNNCell(cells, state_is_tuple=True)

        # Placeholder for input datas, batch_size line, seq_size col
        self.input_data = tf.placeholder(tf.int32,
                                         [self.params.batch_size,
                                          self.params.seq_size])
        # Placeholder for target datas, batch_size line, seq_size col
        self.targets = tf.placeholder(tf.int32,
                                      [self.params.batch_size,
                                       self.params.seq_size])
        # Initial_state for all batches
        self.initial_state = self.cell.zero_state(self.params.batch_size,
                                                  tf.float32)

        # Embedding for our characters. We choose to use simili-words embedding
        # rather than one-hoted vector of len 89. For our format of file,
        # wich has only 89 possible characters, the second one would certainly
        # be better but if we want to train on new type of file, we could have
        # more characters
        self.embedding = tf.Variable(tf.random_uniform(
                                        [len(self.params.chars),
                                         self.params.layer_size],
                                        minval=-1,  maxval=1))

        # Looking for the good embedding for our inputs
        # inputs is tensor of dim [batch_size, seq_size, layer_size]
        inputs = tf.nn.embedding_lookup(self.embedding, self.input_data)
        # Split seq
        # inputs is a list of len seq_size of tensor of shape
        # [batch_size, 1, layer_size]
        inputs = tf.split(inputs, self.params.seq_size, 1)
        # Get off the 1 shape of tensor, wich lead us to ..
        # inputs is a list of len seq_size of tensor of shape
        # [batch_size, layer_size]
        inputs = [tf.squeeze(input_, [1]) for input_ in inputs]

        # Last weight and bias
        w_out = tf.Variable(tf.random_normal([self.params.layer_size,
                                              len(self.params.char_to_key)]))
        b_out = tf.Variable(tf.random_normal([len(self.params.char_to_key)]))

        # Decode our RNN, get outputs and final_state
        outputs, self.final_state = tfcontrib.legacy_seq2seq.rnn_decoder(
                inputs, self.initial_state, self.cell)
        # Get outputs to be of vectors of len layer_size, concatenate these
        # vectors in a matrix (nb of row = batch_size * seq_size)
        output = tf.reshape(tf.concat(outputs, 1),
                            [-1, self.params.layer_size])

        # feedforward simple softmax to get outputs
        self.logits = tf.matmul(output, w_out) + b_out
        self.probs = tf.nn.softmax(self.logits)[0]

        # Get the Weighted cross-entropy loss
        self.loss = tfcontrib.legacy_seq2seq.sequence_loss_by_example(
                 [self.logits],
                 [tf.reshape(self.targets, [-1])],
                 [tf.ones([self.params.batch_size * self.params.seq_size])])

        # Get the mean of the loss
        self.cost = tf.reduce_mean(self.loss)

        # Learning rate, intialize to zero since we're gonna change
        # him manually in train.py
        self.lr = tf.Variable(0.0, trainable=False)

        # AdamOptimizer
        optimizer = tf.train.AdamOptimizer(self.lr)

        # Tell the Optimizer to minimize the cost
        self.train_op = optimizer.minimize(self.cost)

    def sample(self, sess, n):
        # Init state
        state = sess.run(self.cell.zero_state(1, tf.float32))

        # Treat the first chars
        for char in sample_params.first_chars[:-1]:
            data = [[self.params.char_to_key[char]]]
            feed = {self.input_data: data, self.initial_state: state}
            [state] = sess.run([self.final_state], feed)

        # txt we'll be our sample text
        txt = sample_params.first_chars
        count_space = 0
        print('Start sampling ..')

        # Random parameters, rand is big -> the model must be very sure to
        # play a note, (We take probability of playing something (0<p<1)
        # and we take p^rand)
        rand = np.random.normal(sample_params.mu, sample_params.sigma)

        # Sampling
        while count_space < n:
            # We take data as the last char we chose
            data = [[self.params.char_to_key[txt[-1]]]]
            feed = {self.input_data: data, self.initial_state: state}
            # Get the probs, update the state
            [probs, state] = sess.run([self.probs, self.final_state], feed)
            probs = probs**rand
            # Weighted choice in probs
            pred = np.random.choice(self.params.chars,
                                    p=(1/np.sum(probs)) * probs)

            if pred == self.params.separation_char:
                count_space += 1
            print('\r%s/%s %s' % (count_space, int(n), pred),  end=' ')
            txt += pred
        print('Done !')

        return txt
