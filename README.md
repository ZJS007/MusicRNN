# MusicRNN
## LSTM-RNN for Music Generation based on Tensorflow and Python

# WORK IN PROGRESS

# I'll list all references later, but the main ones are :
* Karpathy's char-rnn https://github.com/karpathy/char-rnn;
* Tensroflow char-rnn https://github.com/sherjilozair/char-rnn-tensorflow;
* Hexahedria Recurent neural network for music http://www.hexahedria.com/2015/08/03/composing-music-with-recurrent-neural-networks/ . 

### I'll try to use high level music format to train the network. The format i'll use will probably be the ASCII Musical Notation (AMN) wich is a new format developped by the _Laboratoire Bordelais de Recherche en Informatique_ and the _Conservatoire de Bordeaux_.  

# How to USE

### Dependecies
* Python 3.5+ https://www.python.org/;
* mido library https://pypi.python.org/pypi/mido;  
* numpy for python 3.5+ http://www.numpy.org/;  
* tensorflow for python 3.5+ https://www.tensorflow.org.

#### Step 1
Fill __midis__ folder wither FOLDER(S) containaing .mid or .MID files with a constant BPM of 120 (if you don’t know what BPM is .. it’s ok).

#### Step 2
Then (you can) check if your midis are at 120 BPM and that notes are in the right interval by running __check\_all\_midis.py__.

#### Step 3
Now you will modify the __config.ini file__ for the training phase:  
I recommand you don't touch __NEW\_MIDI\_PARAMETERS__ and __FORMAT\_PARAMETERS__, except if you want to use ONLY 60 bpm (or other tempo) files, then set __bpm__ to be equal to whatever tempo you want.  
Most of __MODEL\_PARAMETERS__ are self explanatory (if you know some about deep learning), be sure to set __init\_from\_model__ to whatever model you want to continue the training, and if you start a new training from scratch, the line should be 'init\_from\_model', to set __init\_from\_model__ to _None_.  
Be sure to change __model\_save\_name__ to the name you want your model to be saved at each step of the training.   
__folder\_name\_list__ must contain name of the folder(s) containing your midi files, separate by semicolons (';')).  

#### Step 4
You can then run __train.py__ wich will automatically turn your midi files into txt data files and then start the training, following your instructions given in config.ini.

#### Step 5
Now you will modify the __config.ini__ file for the sample phase:   
In __SAMPLE\_PARAMETERS__, __n__ is the time your sample will last, in seconds.   
With __first\_chars__ you can force the model to play some note of your choice by enterring the starting characters you want.   
__sample\_from\_model__ should be set to be equal to the name of the model you want to sample from (the name you gave with __model\_save\_name__ in training phase.   
__sample\_dir__ and __sample\_name__ are simply dir and name of the .mid file wich will be created.   
__mu__ and __sigma__ are used to tell the model the degree of confidence it should have in playing a note before actually playing it.   

Basically how it is made is we take A a realization of the Normal distribution of parameters mu and sigma, and at each step, we        perfom weighted choice in the vector of probabilities given by our network at the power of A and normalized so it sums to 1. Since      this is a probability vector, we have the following properties :   
* if A = 1, the vector remain the same, so we can interpret that as 'vanilla' sampling;   
* if A < 1, difference between low value and high value will be lowered, wich can be interpreted as lowering the threshold of          confidence the network must have to play a note;    
* if A > 1, difference between low value and high value will be upped, wich can be interpreted as uping the threshold of             confidence the network must have to play a note.

#### Step 6
Finally you can sample your music from your network by running __sample.py__, wich will do accordingly to what you set up in __config.ini__.   
Most likely, you'll find your .mid file in the sample folder, and it will be named sample.mid.

#### Additional Step
If you want to be sure that the phase .mid -> .txt is working, you can turn all your data to .txt by running __read\_all__ function of the __MusicLoader__ class in the __midi\_interaction.py__ file, and then re-turn this .txt files into midi by running __to\_midi\_all__ of the same object. .mid files will be find in __re\_transformd\_midi__ folder.


# To come later :
## Theory
#### Artificial Neural Networks
#### Recurent neural networks and LSTM
#### Music Format
#### A little bit of maths behind it (at least what I understand)
#### Global architecture
## Results
## Aditionnal Comments, Discussion
