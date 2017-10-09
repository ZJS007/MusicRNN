import mido
import os
from parameters import model_params, sample_params, new_midi_params
import numpy as np

class MusicLoader(object):

    def __init__(self, lowerbound=21,
                 upperbound=108):
        self.lowerbound, self.upperbound = lowerbound, upperbound
        self.span = self.upperbound-self.lowerbound + 1

    def to_text_from_midi(self, midifile):
        matrix = self.to_matrix_from_midi(midifile)
        if matrix == None : 
            return None
        txt = ''
        for line in matrix:
            chars = [model_params.key_to_char[i] 
                        for i, x in enumerate(line) if x == 1]
            for char in chars:
                txt += char
            txt += model_params.separation_char
        while txt[0] == model_params.separation_char:
            txt = txt[1:]
        while txt[-1] == model_params.separation_char:
            txt = txt[:-1]
        txt = model_params.separation_char + txt + model_params.separation_char
        return txt

    def get_tracks_with(self, pattern, evt_type):
        tracks = []
        for track in pattern.tracks:
            for evt in track:
                if evt.type == evt_type:
                    tracks.append(track)
                    break
        return tracks

    def to_midi_from_text(self, textfile,
                          name = sample_params.sample_name,
                          dir_ = sample_params.sample_dir):
        print('Turning %s into midi ..' % textfile, end= ' ')
        text = open(textfile, 'r').read()
        matrix = []
        for chunk in text.split(model_params.separation_char):
            indexes = [model_params.char_to_key[char] for char in chunk]
            line = [1 if i in indexes else 0 for i in range(88)]
            matrix.append(line)
        midipattern = self.to_midi_from_matrix(matrix)
        self.save_midi_file(midipattern, name = name, dir_ = dir_)
        print('Done !')
        
    def save_midi_file(self, midipattern,
                       name = sample_params.sample_name,
                       dir_ = sample_params.sample_dir):
        midipattern.save("%s/%s.mid"%(dir_, 
                                         name))

    def to_matrix_from_midi(self, midifile):
        pattern = mido.MidiFile(midifile)
        tracks = self.get_tracks_with(pattern, 'note_on')

        adjust_tick_coeff = pattern.ticks_per_beat // new_midi_params.new_resolution
        for track in tracks:
            for i, evt in enumerate(track):
                while evt.time % (adjust_tick_coeff) != 0:
                    if evt.time % (adjust_tick_coeff) > adjust_tick_coeff // 2:
                        evt.time += 1
                        if i+1 != len(track) : track[i+1].time -= 1
                    elif evt.time % (adjust_tick_coeff) <= adjust_tick_coeff // 2:
                        evt.time -= 1
                        if i+1 != len(track) : track[i+1].time += 1
                evt.time= int(evt.time/adjust_tick_coeff)

        matrixes = []
        for track in tracks:
            matrix = [[0 for _ in range(self.span)] for _ in range(2)]
            for evt in track:
                
                timeleft = evt.time
                while timeleft > 0:  
                    oldstate = [ele for ele in matrix[-1]]
                    matrix.append(oldstate)
                    timeleft -= 1      
                if evt.type == 'note_on' or evt.type == 'note_off':
                    evt.note = evt.note - self.lowerbound
                    if evt.type == 'note_on' and evt.velocity != 0 :
                        if matrix[-2][evt.note] == 1:
                            matrix[-2][evt.note] = 0
                        matrix[-1][evt.note] = 1
                    elif evt.type == 'note_off' or evt.velocity == 0:
                        matrix[-1][evt.note] = 0
            matrixes.append(matrix)

        fusion_matrix = [list(sum(np.asarray(z))) for z in zip(*matrixes)]

        return fusion_matrix
        
    def to_midi_from_matrix(self, matrix):
        
        matrix_prev = [[0 for _ in range(self.span)]] + matrix[:-1]
        
        pattern = mido.MidiFile()
        pattern.ticks_per_beat = 16
        track = mido.MidiTrack()
        pattern.tracks.append(track)

        track.append(mido.MetaMessage('set_tempo', tempo = mido.bpm2tempo(120), time=0))
        last_event_tick = 0
        for tick, (state, previous_state) in enumerate(zip(matrix, matrix_prev)):
            offNotes, onNotes = [], []
            for pitch, (n, p) in enumerate(zip(state, previous_state)):
                if p == 1 and n == 0:
                    self.add_note_off_event(track, tick-last_event_tick, pitch+self.lowerbound)
                    last_event_tick = tick
                elif p == 0 and n == 1:
                    self.add_note_on_event(track, tick-last_event_tick, pitch+self.lowerbound)
                    last_event_tick = tick
                if tick == len(matrix) - 1 and n == 1:
                    self.add_note_off_event(track, tick-last_event_tick, pitch+self.lowerbound)
                    last_event_tick = tick
        track.append(mido.MetaMessage('end_of_track', time=last_event_tick + 1))
        return pattern

    def add_note_off_event(self, track, tick, pitch):
        track.append(mido.Message('note_off', note=pitch, velocity=127, time=tick))
                                          
    def add_note_on_event(self, track, tick, pitch):
        track.append(mido.Message('note_on', note=pitch, velocity=50, time=tick))
        

    def read_all(self):
        if model_params.midis_folder_name_list == 'all':
            model_params.midis_folder_name_list = os.listdir('midis')
        n = 0
        for folder in model_params.midis_folder_name_list:
            n += len(os.listdir('midis/'+folder))
        print('Turning midis into .txt data ..')
        count = 0
        for folder in model_params.midis_folder_name_list:
            for name in os.listdir('midis/'+folder):
                if name[-4:].lower() == '.mid':
                    txt = self.to_text_from_midi('midis/'+folder+'/'+name)
                    file_ = open('data/%s.txt'%name[:-4], 'w')
                    file_.write(txt)
                    file_.close()
                count += 1
                print('\r%s/%s' % (count, n), end=' ')
        print('Done !')
        
    def to_midi_all(self):
        for name in os.listdir('data'):
            if name[-4:] == '.txt':
                self.to_midi_from_text('data/'+name, name = name[:-4], dir_ = 're_transformed_midi')

    def check_if_pattern_is_ok(self, pattern, tempo):
        for track in pattern.tracks:
            for evt in track:
                if evt.type == 'set_tempo':
                    if mido.tempo2bpm(evt.tempo) != tempo :
                        return False
                elif evt.type == 'note_on':
                    if not self.lowerbound < evt.note < self.upperbound:
                        return False
        return True

    def check_all_midi(self):
        n = 0
        for folder in os.listdir('midis'):
            n += len(os.listdir('midis/'+folder))
        print('Checking if your midis are at 120 BPM and notes are OK ..')
        count = 0
        for folder in os.listdir('midis'):
            for name in os.listdir('midis/'+folder):
                if name[-4:].lower() == '.mid':
                    try:
                        pattern = mido.MidiFile('midis/'+folder+'/'+name)
                    except:
                        try :
                            os.remove('midis/'+folder+'/'+name)
                        except:
                            print(name, 'problem : need manual supr')
                    if not self.check_if_pattern_is_ok(pattern, 120):
                        os.remove('midis/'+folder+'/'+name)
                count += 1
                print('\r%s/%s' % (count, n), end= ' ')
        print('Done !')

    def clear_data(self):
        print('Clearing data ..')
        for name in os.listdir('data'):
            os.remove('data/'+name)
        print('Done !')


