import os
import tensorflow as tf
import numpy as np
from text_loader import TextLoader
from model import Model
from parameters import model_params
from midi_interaction import MusicLoader
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def train():

    """ Train Action """

    # Our model
    model = Model(model_params)

    with tf.Session() as sess:

        sess.run(tf.global_variables_initializer())
        saver = tf.train.Saver(tf.global_variables())

        # Init from already existing model, if any
        if model_params.init_from_model is not None:
            checkpoint = tf.train.get_checkpoint_state(
                            'model_saved/%s' % model_params.init_from_model)
            saver.restore(sess, checkpoint.model_checkpoint_path)
            print('Model restored !')
        print('Start training ..')
        dir_ = os.listdir('data')
        data_loaders = []

        # Load texts via DataLoader object
        for f in dir_:
            if f[-4:] == '.txt':
                data_loader = TextLoader(f,
                                         model_params.batch_size,
                                         model_params.seq_size)
                data_loaders.append(data_loader)

        # Training phase

        # We will make n_epoch epochs
        for e in range(model_params.n_epoch):
            n_f_done = 0
            for data_loader in data_loaders:
                print('Epoch %s  %s / %s' % (e, n_f_done, len(dir_)), end='\r')
                # Get at start of file
                data_loader.reset_batch_pointer()

                # Assign learning rate to be learning_rate / sqrt(n_batches), the
                # number of batches in this text. So training on 1 min piece
                # has ~ the same impact as training on 1 hour piece.
                sess.run(tf.assign(model.lr,
                         (model_params.learning_rate /
                          int(np.sqrt(data_loader.n_batches)))))

                # Init state
                state = sess.run(model.initial_state)

                # For all batches
                for b in range(data_loader.n_batches):
                    data, target = data_loader.get_next_batch()

                    # We will feed data, target, and state (we update state
                    # component manually) state for all neuron will be a tuple
                    # (c, h), this is relative to how LSTM works
                    feed = {model.input_data: data, model.targets: target}
                    for i, (c, h) in enumerate(model.initial_state):
                        feed[c] = state[i].c
                        feed[h] = state[i].h

                    # Do training operation
                    _ = sess.run([model.train_op], feed)

                n_f_done += 1

            # Save model
            saver.save(sess, 'model_saved/%s/model.checkpoint' %
                       model_params.model_save_name)
            print("""End of epoch %s Model Saved""" %
                  e)
        print('Done !')

if __name__ == '__main__':
    stop = False
    if model_params.init_from_model is not None:
        if model_params.init_from_model not in os.listdir('model_saved'):
            stop = True
            print("You try to init from a model that doesn't exists")
    print("""You start a new training, do you want to clear already
            existing data files ? [Y/N]""", end=' ')
    choice = input()
    if choice == 'Y' or choice == 'y':
        music_loader = MusicLoader()
        music_loader.clear_data()
    elif choice == 'N' or choice == 'n':
        pass
    else:
        input('[Y/N] :')
    if model_params.init_from_model is None:
        if model_params.model_save_name in os.listdir('model_saved'):
            print("""You start a new training from scratch, but there is
                  already a model with the name you chose, do you want to
                  delete it ? [Y/N]'""", end=' ')
            choice = input()
            if choice == 'Y' or choice == 'y':
                pass
            elif choice == 'N' or choice == 'n':
                stop = True
                print('Please choose another name in the config.ini file')
            else:
                input('[Y/N] :')
        if model_params.model_save_name not in os.listdir('model_saved'):
            os.makedirs('model_saved/%s' % model_params.model_save_name)

    if not stop:
        if os.listdir('data') == []:
            print('Found data dir empty, reading midis ..')
            music_loader = MusicLoader()
            music_loader.read_all()

        train()
