
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
import pdb


def fillStimNames(sylb,spaCond,tarDir,codei,intDir):
    sylbDir = getSylbDir(tarDir,codei,intDir)
    if codei == 'I':
        file_name = '../stimuli/' + sylb + '_' + sylbDir + '_' + spaCond + '_5db.wav' 
    else:
        file_name = '../stimuli/' + sylb + '_' + sylbDir + '_' + spaCond + '.wav'
    return file_name

def getSylbDir(tarDir,codei,intDir):
    if codei == 'T':
        sylbDir = tarDir
    elif codei == 'D':
        if tarDir == '30L':
            sylbDir = '30R'
        elif tarDir == '30R':
            sylbDir = '30L'
        else:
            raise ValueError
    elif codei == 'I':
        if intDir == 'cont':
            if tarDir == '30L':
                sylbDir = '90R'
            elif tarDir == '30R':
                sylbDir = '90L'
            else:
                raise ValueError
        elif intDir == 'ips':
            if tarDir == '30L':
                sylbDir = '90L'
            elif tarDir == '30R':
                sylbDir = '90R'
            else:
                raise ValueError
        else:
            raise ValueError
    return sylbDir


def genTrigger(stream, trig, spaCond='HRTF',tarDir='30L',intCond='cont'):
    cue_ontset = 0.5
    sylb_time = 0.45
    str_isi = 0.3
    str_onset = cue_ontset + sylb_time + 0.5
    
    # time list 
    if len(stream) == 6: # uninterrupted
        codes = ['T','D','T','D','T','D']
        onset_time = np.arange(6)*str_isi + str_onset 
        # if onset_time is list, T2 time would be 2.3499999999999996 instead of 2.35, why?
    elif len(stream) == 7: # interrupted
        codes = ['T','D','I','T','D','T','D']
        int_time = 1.925 # str_onset + str_isi*2 - 0.125
        onset_time = np.arange(6)*str_isi + str_onset
        onset_time = np.insert(onset_time,2,int_time)
    else:
        print('stream length not right')
        raise ValueError
    
    #cue_mat,fs = medussa.read_file(fillStimNames('ba',spaCond,tarDir,'T',intCond)) 
    cue_mat,fs = sf.read(fillStimNames('ba',spaCond,tarDir,'T',intCond))
    # medussa.play_array(cue_mat,fs,output_device_id=16) 

    total_time = np.max(onset_time) + sylb_time + 0.5
    total_len = int(total_time*fs)
    
    cue_pad = np.pad(cue_mat,((int(cue_ontset*fs),int((total_time-cue_ontset-sylb_time)*fs)),(0,0)),'constant',constant_values=0)
    
    full_stream = cue_pad 
    tar_stream = cue_pad
    for i in range(len(stream)):
        #stim_mat,fs = medussa.read_file(fillStimNames(stream[i],spaCond,tarDir,codes[i],intCond))
        stim_mat,fs = sf.read(fillStimNames(stream[i],spaCond,tarDir,codes[i],intCond))

        pad_s = int(onset_time[i]*fs)
        pad_e = int(full_stream.shape[0] - pad_s - stim_mat.shape[0])
        stim_pad = np.pad(stim_mat,((pad_s,pad_e),(0,0)),'constant',constant_values=0)

        full_stream = full_stream + stim_pad

        # build target stream for third channel (can remove if not necessary)
        if codes[i] == 'T':
            tar_stream = tar_stream + stim_pad
    
    # if use third channel for timing
    trig_chan = np.zeros((full_stream.shape[0],1))
    trig_dur = 100
    trig_chan[0:trig_dur] = 1 # visual stimuli on
    trig_chan[int(cue_ontset*fs):int(cue_ontset*fs)+trig_dur] = 0.5 # cue time
    #trig_chan[(onset_time*fs).astype(int)] = 0.5 # audio time
    for ot in onset_time:
        trig_chan[int(ot*fs):int(ot*fs)+trig_dur] = 0.5
    
    # condition code: using channel 3 is based on the assumption that at least the recorded onset time is accurate
    trig_onset = 1000
    trig_interval = 100
    trig_s = int(trig_onset+trig*trig_interval)
    trig_chan[trig_s:trig_s+trig_dur] = 1 # TODO: check this # 1=>1100:1200   2: 1200:1300, decode: (onset_time-1000)/100

    tar_chan = tar_stream[:,np.argmax(np.max(tar_stream,axis=0))].reshape(-1,1) 
    trig_chan = trig_chan + tar_chan

    #pdb.set_trace()

    plt.plot(trig_chan)
    plt.show()



if __name__ == '__main__':
    stream = ['ba','da','meow','da','da','ga','ga']#['ba','da','meow','ba','da','ba','da']
    trig = 3
    genTrigger(stream,trig)
