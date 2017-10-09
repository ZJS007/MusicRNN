# MusicRNN
LSTM-RNN for Music Generation based on Tensorflow

# WORK IN PROGRESS

# I'll list all references later, but the main ones are :
• Karpathy's char-rnn https://github.com/karpathy/char-rnn
• Tensroflow char-rnn https://github.com/sherjilozair/char-rnn-tensorflow
• Hexahedria Recurent neural network for music http://www.hexahedria.com/2015/08/03/composing-music-with-recurrent-neural-networks/

### I'll try to use high level music format to train the system. The format i'll use will probably be the ASCII Musical Notation (AMN) wich is a new format developped by the Laboratoire Bordelais de Recherche en Informatique and the Conservatoire de Bordeaux.

# How to USE

### Dependecies

• mido library https://pypi.python.org/pypi/mido;
• numpy for python 3.5+ http://www.numpy.org/;
• tensorflow for python 3.5+ https://www.tensorflow.org

##### Step 1
Fill midis folder wither FOLDER(S) containaing .mid or .MID files with a constant BPM of 120 (if you don’t know what BPM is .. it’s ok);

##### Step 2
Then (you can) check if your midis are at 120 BPM and that notes are in the right interval by running check_all_midis.py;

##### Step 3
Specify your model parameters into the config.ini file (specially, folder_name_list must contain name of the folder(s) containing your midi files, sperate by semicolon;)

##### Step 4
You can the run train.py wich will automatically turn your midi files into txt data files and then start the training, following your instructions given in config.ini;

##### Step 5
Once training is done, you can command your model to compose something by running sample.py (you may want to modify sample parameters in the config.ini file)
