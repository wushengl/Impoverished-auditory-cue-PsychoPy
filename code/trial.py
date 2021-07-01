#from psychopy import prefs
#prefs.hardware['audioLib'] = ['PTB'] 

from psychopy import visual, event #, sound, parallel, core
#import psychtoolbox as ptb
import numpy as np 
import random
import time
import pdb

import serial
import serial.tools.list_ports
import medussa

import matplotlib.pyplot as plt

device = medussa.open_device(16,16,8)


'''
port_list = list(serial.tools.list_ports.comports())


if len(port_list) <= 0:
    print("Couldn't find serial port!")
else:
    port_list_0 =list(port_list[0])
    port_serial = port_list_0[0]

    global port
    port = serial.Serial(port_serial,9600)
'''


# press 'r' to repeat or click on button?
# https://discourse.psychopy.org/t/how-to-play-and-repeat-stimuli-after-manual-click/4845

#parallel.setPortAddress(0x378)  # address for parallel port on many machines
#pinNumber = 2  # choose a pin to write to (2-9).

# int and bytes
# zzz = 253
# zzz.to_bytes(1,'little')
# int.from_bytes(zzz.to_bytes(1,'little'),'little')


def runTrial(win,trialCond,ti,total,corrCount,isTrain=True): 
    
    spaCond = trialCond['spaCond']
    tarDir = trialCond['tarDir']
    intCond = trialCond['intCond'] # this is None for training trial
    
    trialInfo = generateTrial(trialCond) 
    playTrial(win,trialInfo)
    response = collectResponse(win,ti,total) 
    trialInfo['response'] = response
    
    if isTrain: 
        results, corrCount = feedbackScreen(win,trialInfo,corrCount,total)
    else:
        results = getResult(trialInfo)
        if np.sum(results) == 3:
            corrCount += 1
    
    trialInfo['results'] = results
    
    return trialInfo, corrCount


def getResult(trialInfo):
    
    targets = np.array(trialInfo['targets']) 
    syllables = np.array(['ba','da','ga']) 
    resp = trialInfo['response']
    responses = syllables[resp]
    
    results = (responses == targets).astype(int)
    
    return results


def feedbackScreen(win,trialInfo,corrCount,total):
    
    targets = np.array(trialInfo['targets']) 
    results = getResult(trialInfo)
    
    if np.sum(results) == 3:
        trialPass = 'have passed'
        corrCount += 1
    else:
        trialPass = 'didn\'t pass'
    
    feedback = 'The correct answer is ' + targets[0] + ', ' + targets[1] + ', ' + targets[2] + '.\n'\
            'You ' + trialPass + ' this trial. \n'\
            'Press Space to move on.'
    txt = visual.TextStim(win,text=feedback)
    
    corrTxt = 'Current training score: ' + str(corrCount) + '/' + str(total)
    txt_corr = visual.TextStim(win,text=corrTxt,pos=[0,-0.5])
    
    txt.draw()
    txt_corr.draw()
    win.flip()
    
    event.waitKeys(keyList=['space'])
    
    return results, corrCount


def collectResponse(win,ti,total):
    
    crtTrial = 'Current Trial: ' + str(ti) + '/' + str(total)
    txt_trial = visual.TextStim(win,text=crtTrial,pos=[0.65,-0.8],height=0.08)
    
    inst = 'Click on the syllables you heard from the target direction, press Space to move on.'
    txt = visual.TextStim(win,text=inst,pos=[0,0.6])
    
    s1 = '1st Syllable: '
    s2 = '1st Syllable: '
    s3 = '1st Syllable: '
    txt_s1 = visual.TextStim(win,text=s1,pos=[-0.6,0.2],height=0.08)
    txt_s2 = visual.TextStim(win,text=s2,pos=[-0.6,-0.05],height=0.08)
    txt_s3 = visual.TextStim(win,text=s3,pos=[-0.6,-0.3],height=0.08)
    
    scaleSetting = {
        'win': win,
        'low': 0,
        'high': 2,
        'labels': ['ba','da','ga'],
        'marker': 'circle',
        'lineColor': 'grey',
        'scale': None,
        'mouseOnly': True,
        'showAccept': False,
        'singleClick': True
    } # 'acceptKeys': 'space'
    sylbScale1 = visual.RatingScale(pos=[0,0.25], **scaleSetting)
    sylbScale2 = visual.RatingScale(pos=[0,0], **scaleSetting)
    sylbScale3 = visual.RatingScale(pos=[0,-0.25], **scaleSetting)
    
    txt_trial.draw()
    txt.draw()
    txt_s1.draw()
    txt_s2.draw()
    txt_s3.draw()
    sylbScale1.draw()
    sylbScale2.draw()
    sylbScale3.draw()
    
    win.flip()
    
    while sylbScale1.noResponse or sylbScale2.noResponse or sylbScale3.noResponse or ('space' not in event.getKeys(keyList=['space'])):
        txt_trial.draw()
        txt.draw()
        txt_s1.draw()
        txt_s2.draw()
        txt_s3.draw()
        sylbScale1.draw()
        sylbScale2.draw()
        sylbScale3.draw()
        win.flip()
    
    res1 = sylbScale1.getRating()
    res2 = sylbScale2.getRating()
    res3 = sylbScale3.getRating()
    
    response = [res1,res2,res3]
    
    return response


def generateTrial(trialCond):
    '''
    This function is used for generating one trial with given conditions:
        - HRTF/ILD/ITD
        - interrupted/not interrupted
        - target left/right
    Input:
        - tarDir: target direction in string, e.g. '30L'
        - intCond: interrupter condition, could be None or 'meow'
    Return:
        - trialInfo: e.g. {'tarDir': '30L', 
            'intCond' = 'meow', 
            'targets': ['ba','da','ga'], 
            'distractors': ['da','da','ga'], 
            'stream': ['ba','da','meow','da','da','ga','ga']}

        * by saving targets and distractors in short version can make it easier for later analysis, making stream full name and 
        in the right order can make it easier for playing the stimuli
    '''
    
    spaCond = trialCond['spaCond']
    tarDir = trialCond['tarDir']
    intCond = trialCond['intCond']
    
    Ts = randomStream()
    Ds = randomStream()
    
    if intCond:
        intSti = 'meow'
    else:
        intSti = None
    
    stream = [Ts[0],Ds[0],intSti,Ts[1],Ds[1],Ts[2],Ds[2]]
    stream = [stimulus for stimulus in stream if stimulus] # if interupter is None, remove it

    trig = getTriggerCode(spaCond,intCond,tarDir)
    
    trialStim = {
        'spaCond': spaCond,
        'tarDir': tarDir,
        'intCond': intCond,
        'targets': Ts,
        'distractors': Ds,
        'stream': stream,
        'trigger': trig
    }
    
    return trialStim

def playTrial(win,trialStim):
    
    spaCond = trialStim['spaCond']
    tarDir = trialStim['tarDir']
    intCond = trialStim['intCond']
    stream = trialStim['stream']
    trig = trialStim['trigger']

    # timing for audio stimuli
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
    
    cue_mat,fs = medussa.read_file(fillStimNames('ba',spaCond,tarDir,'T',intCond)) 
    # medussa.play_array(cue_mat,fs,output_device_id=16) 

    total_time = np.max(onset_time) + sylb_time + 0.5
    total_len = int(total_time*fs)
    
    cue_pad = np.pad(cue_mat,((int(cue_ontset*fs),int((total_time-cue_ontset-sylb_time)*fs)),(0,0)),'constant',constant_values=0)
    
    full_stream = cue_pad 
    tar_stream = cue_pad
    for i in range(len(stream)):
        stim_mat,fs = medussa.read_file(fillStimNames(stream[i],spaCond,tarDir,codes[i],intCond))

        pad_s = int(onset_time[i]*fs)
        pad_e = int(full_stream.shape[0] - pad_s - stim_mat.shape[0])
        stim_pad = np.pad(stim_mat,((pad_s,pad_e),(0,0)),'constant',constant_values=0)

        full_stream = full_stream + stim_pad

        # build target stream for third channel (can remove if not necessary)
        if codes[i] == 'T':
            tar_stream = tar_stream + stim_pad
    
    # if use third channel for timing
    trig_chan = np.zeros((full_stream.shape[0],1))
    trig_chan[0:200] = 1 # visual stimuli on
    trig_chan[int(cue_ontset*fs):int(cue_ontset*fs)+200] = 0.5 # cue time
    trig_chan[(onset_time*fs).astype(int)] = 0.5 # audio time
    trig_chan[trig] = 1 # TODO: check this
    tar_chan = tar_stream[:,np.argmax(np.max(tar_stream,axis=0))].reshape(-1,1) 
    trig_chan = trig_chan + tar_chan

    full_stream = np.concatenate((full_stream,trig_chan),axis=1)

    '''
    # if adding EEG triger to the audio channels (1&2) as clicks, 
    # not using this because the trigger is audible and would lead to an unwanted response in EEG

    # option 1: simple square wave
    trig_chan = np.zeros((total_len,2))
    trig_chan[0:45,:] = np.max(full_stream)*0.3 # change length and amplitude here
    
    # option 2: tone pip
    f = 1000
    fs = 44100
    duration = 50/1000
    x = np.arange(int(fs*duration))
    y = np.sin(2*np.pi*x*f/fs).astype(np.float32)
    ramp = y*np.hamming(len(y))*0.3*np.max(full_stream)

    trig_chan = np.pad(ramp,(0,total_len-ramp.shape[0]),'constant',constant_values=0).reshape(-1,1)
    trig_chan = np.concatenate((trig_chan,trig_chan),axis=1)
    
    full_stream = full_stream + trig_chan
    '''

    cross = visual.TextStim(win=win,text='+',height=0.3)
    cross.draw() 
    #win.callOnFlip(port.write,trig.to_bytes(1,'little')) # TODO: add more info? the target sequence and the response?
    win.flip() 

#    print("***********************************************************")
#    print(np.max(full_stream[:,2]))
#    print("***********************************************************")
#    plt.plot(full_stream[:,2])
#    plt.show()


    #medussa.play_array(full_stream,fs,output_device_id=16) 
    s = device.open_array(full_stream, fs)
    s.play()
    while s.is_playing: 
        time.sleep(0.01)

    '''
    # play one-by-one
    time_trial = []
    for i in range(len(stream)):
        time_trial.append(timer.getTime())
        medussa.play_array(stimuli[i],fs)
        time.sleep(timeList[i]) 
    time.sleep(0.5) 
    '''


def randomStream():
    '''
    This function is used for generating one random stream, each syllable could be ba/da/ga with replacement.
    '''
    sylbOptions = ['ba','da','ga']
    stream = [sylbOptions[random.randint(0,2)],sylbOptions[random.randint(0,2)],sylbOptions[random.randint(0,2)]]
    
    return stream


def fillStimNames(sylb,spaCond,tarDir,codei,intDir):
    sylbDir = getSylbDir(tarDir,codei,intDir)
    if codei == 'I':
        file_name = '../stimuli/' + sylb + '_' + sylbDir + '_' + spaCond + '_5dB.wav' 
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
