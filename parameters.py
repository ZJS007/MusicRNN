from config import config

class Stock(object):
    def __init__(self, **kwargs):
        for name in kwargs:
            setattr(self, name, kwargs[name])

chars = tuple(config['FORMAT_PARAMETERS']['note_chars']) + tuple(config['FORMAT_PARAMETERS']['separation_char'])
char_to_key = dict(zip(chars, range(89)))
key_to_char = dict(zip(range(89), chars))

notes = ('A_1', 'Bb_1', 'B_1', 'C_2', 'Db_2', 'D_2', 'Eb_2', 'E_2',
         'F_2', 'Gb_2', 'G_2', 'Ab_2', 'A_2', 'Bb_2', 'B_2', 'C_3',
         'Db_3', 'D_3', 'Eb_3', 'E_3', 'F_3', 'Gb_3', 'G_3', 'Ab_3',
         'A_3', 'Bb_3', 'B_3', 'C_4', 'Db_4', 'D_4', 'Eb_4', 'E_4',
         'F_4', 'Gb_4', 'G_4', 'Ab_4', 'A_4', 'Bb_4', 'B_4', 'C_5',
         'Db_5', 'D_5', 'Eb_5', 'E_5', 'F_5', 'Gb_5', 'G_5', 'Ab_5',
         'A_5', 'Bb_5', 'B_5', 'C_6', 'Db_6', 'D_6', 'Eb_6', 'E_6',
         'F_6', 'Gb_6', 'G_6', 'Ab_6', 'A_6', 'Bb_6', 'B_6', 'C_7',
         'Db_7', 'D_7', 'Eb_7', 'E_7', 'F_7', 'Gb_7', 'G_7', 'Ab_7',
         'A_7', 'Bb_7', 'B_7', 'C_8', 'Db_8', 'D_8', 'Eb_8', 'E_8',
         'F_8', 'Gb_8', 'G_8', 'Ab_8', 'A_8', 'Bb_8', 'B_8', 'C_9')

note_to_char = dict(zip(notes, chars[:-1]))

new_midi_params = Stock()
for key in config['NEW_MIDI_PARAMETERS']:
    setattr(new_midi_params, key, config['NEW_MIDI_PARAMETERS'][key])

sec_per_beat = 60.0 / new_midi_params.bpm
new_midi_params.tick_per_sec = new_midi_params.new_resolution / sec_per_beat

model_params = Stock()
for key in config['MODEL_PARAMETERS']:
    setattr(model_params, key, config['MODEL_PARAMETERS'][key])
model_params.chars = chars
model_params.char_to_key = char_to_key
model_params.key_to_char = key_to_char
model_params.separation_char = config['FORMAT_PARAMETERS']['separation_char']

sample_params = Stock()
for key in config['SAMPLE_PARAMETERS']:
    setattr(sample_params, key, config['SAMPLE_PARAMETERS'][key])
sample_params.note_to_char = note_to_char
sample_params.n *= new_midi_params.tick_per_sec