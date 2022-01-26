#from psychopy import data, logging, gui, visual
import psychopy
from psychopy import data, gui, visual, event , sound
from psychopy import __version__

import numpy as np
import matplotlib.pyplot as plt

import soundfile
import pdb

import sounddevice as sd


cue_ontset = 0.5
sylb_time = 0.45
str_isi = 0.3
str_onset = cue_ontset + sylb_time + 0.5

onset_time = np.arange(6)*str_isi + str_onset 
codes = ['T','D','T','D','T','D'] 

'''
# test interrupted condition
codes = ['T','D','I','T','D','T','D']
int_time = 1.925 # str_onset + str_isi*2 - 0.125
onset_time = np.arange(6)*str_isi + str_onset
onset_time = np.insert(onset_time,2,int_time)
'''

file = '../stimuli/ba_30R_HRTF.wav'
cue_mat,fs = soundfile.read(file)

total_time = np.max(onset_time) + sylb_time + 0.5
total_len = int(total_time*fs)

cue_pad = np.pad(cue_mat,((int(cue_ontset*fs),int((total_time-cue_ontset-sylb_time)*fs)),(0,0)),'constant',constant_values=0)
    
full_stream = cue_pad
tar_stream = cue_pad


for i in range(len(onset_time)):
    stim_mat = cue_mat
    pad_s = int(onset_time[i]*fs)
    pad_e = int(full_stream.shape[0]-pad_s-stim_mat.shape[0])

    stim_pad = np.pad(stim_mat,((pad_s,pad_e),(0,0)),'constant',constant_values=0)
    full_stream = full_stream + stim_pad

    # build target stream for third channel (can remove if not necessary)
    if codes[i] == 'T':
        tar_stream = tar_stream + stim_pad


trig_chan = np.zeros((full_stream.shape[0],1))
trig_chan[0] = 1 # visual stimuli on
trig_chan[int(cue_ontset*fs)] = 0.5 # cue time
trig_chan[(onset_time*fs).astype(int)] = 0.5 # audio time
tar_chan = tar_stream[:,np.argmax(np.max(tar_stream,axis=0))].reshape(-1,1) 
trig_chan = trig_chan + tar_chan

full_stream = np.concatenate((full_stream,trig_chan),axis=1)

plt.plot(full_stream[:,2])
plt.show()

'''
# option 1
trig_chan = np.zeros((total_len,2))
trig_chan[0:44,:] = 0.3*np.max(full_stream) # 45 samples, about 1ms

# option 2
f = 1000
fs = 44100
duration = 50/1000
x = np.arange(int(fs*duration))
y = np.sin(2*np.pi*x*f/fs).astype(np.float32)
ramp = y*np.hamming(len(y))*0.1*np.max(full_stream)

trig_chan = np.pad(ramp,(0,total_len-ramp.shape[0]),'constant',constant_values=0).reshape(-1,1)
trig_chan = np.concatenate((trig_chan,trig_chan),axis=1)

#plt.plot(ramp)
#plt.show()

final_stream = full_stream + trig_chan
plt.plot(final_stream);plt.show()
'''


sd.play(full_stream[:,2])


def getTriggerCode(spaCond,intCond,tarDir): # TODO: check trigger code before we start
    spaCond_pool = ['HRTF','ITD','ILD']
    intCond_pool = [None,'cont','ips'] 
    tarDir_pool = ['30L','30R']

    code = spaCond_pool.index(spaCond)*len(intCond_pool)*len(tarDir_pool) + intCond_pool.index(intCond)*len(tarDir_pool) + tarDir_pool.index(tarDir)

    return code+1


def test_getTriggerCode():
    spaCond_pool = ['HRTF','ITD','ILD']
    intCond_pool = [None,'cont','ips']
    tarDir_pool = ['30L','30R']

    for spaCond in spaCond_pool:
        for intCond in intCond_pool:
            for tarDir in tarDir_pool:
                code = getTriggerCode(spaCond,intCond,tarDir)
                print(spaCond,intCond,tarDir,code)
    return code 


test_getTriggerCode()
