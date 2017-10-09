import os
import tensorflow as tf
from parameters import model_params, sample_params, new_midi_params
from model import Model
from midi_interaction import MusicLoader
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def sample():
    """ Sample Action """

    # Our model
    model = Model(model_params, in_training=False)

    sess = tf.Session()
    sess.run(tf.global_variables_initializer())

    # Try to get the saved model

    saver = tf.train.Saver(tf.global_variables())
    checkpoint = tf.train.get_checkpoint_state('model_saved/%s' %
                                               sample_params.sample_from_model)

    try:
        saver.restore(sess, checkpoint.model_checkpoint_path)
        print('Model restored !')
    except:
        print("""You need to indicate a valide directory containing a trained
              model in config for sample_from_model""")
        return

    # Get the sample text
    sample_txt = model.sample(sess, sample_params.n)

    # Write it in a .txt file
    file_ = open('%s/%s.txt' % (sample_params.sample_dir,
                                sample_params.sample_name), 'w')
    file_.write(sample_txt)
    file_.close()

if __name__ == '__main__':
    sample()

    # Turn sample text to midi
    music_loader = MusicLoader()
    music_loader.to_midi_from_text('%s/%s.txt' % (sample_params.sample_dir,
                                                  sample_params.sample_name))
