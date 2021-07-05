from psychopy import data, logging, gui, visual, core, event 
from psychopy import __version__

import expInfoGUI
import expInstructions
import makeTrialDictList
import trial

import pdb

import serial
import serial.tools.list_ports
import sys

import medussa 


#pdb.set_trace()
device = medussa.open_device(16,16,8) # input device, ouput device, channel


'''
ExtraInfo:
    - participant: ID input from GUI
    - interrupter: 'both' or 'cont' or 'ips'

TODO:
    1. how to manage participants ID? need to blind?
    2. test by myself with small amount of trials before piloting
    3. need to change trigger code in trial.py if changing conditions
    4. pycord (login with Nike account only?)

    50 ms 1k hz, hamming peak amplitude 0.3 (just know where it is)
'''


# settings and parameters 

condition = ['cont','ips','both'] # interrupter condition
spatialization = ['all','HRTF','ITD','ILD']


ratio = 1/2
trialNum = 480
blockNum = 12
taskBlockLen = int(trialNum/blockNum)
taskSessionLen = 160 # 480/3

expInfo = expInfoGUI.showGUI(condition,spatialization,trialNum=480,blockNum=10)
expDataFile = '../data/ASAExp_' + expInfo['Subject'] + '/ASAExp_' + expInfo['Subject']
trainDataFile = expDataFile + '_train'
taskDataFile = expDataFile + '_task'
expDataFile = expDataFile + '_exp'

trialNum = expInfo['Trial Number']
intCond = expInfo['Condition']
spaCond = expInfo['Spatialization']

trainNum = 6 
trainThre = 4


'''
# TODO: do we still want to use serial port?
port_list = list(serial.tools.list_ports.comports())

if len(port_list) <= 0:
    print("Couldn't find serial port!")
else:
    port_list_0 =list(port_list[0])
    port_serial = port_list_0[0]

    global port
    port = serial.Serial(port_serial,9600) # device name, baudrate (baud-rate)
    #port.open()
'''


exp = data.ExperimentHandler(name='AuditorySpatialAttention',
                version='0.1', 
                extraInfo={'participant':expInfo['Subject'], 'Condition':intCond,'Spatialization':spaCond},
                runtimeInfo=None,
                originPath=None,
                savePickle=True,
                saveWideText=False,
                dataFileName=expDataFile)


win = visual.Window(fullscr=True) # maybe should make win global as well...

# global keys
event.globalKeys.add('escape', func=core.quit)


#####################################################
# train session 
#####################################################

corrCount = 0

while corrCount < trainThre:

    expInstructions.showInstruction(win)
    expInstructions.train_critInstruction(win)

    trainConds = makeTrialDictList.makeTrialDictList(spaCond='HRTF',isTrain=True,trialNum=trainNum) 
    training = data.TrialHandler(trialList=trainConds, nReps=1, name='train', method='random')  # didn't use seed here since we want each training to be different
    exp.addLoop(training)

    ti = 0
    corrCount = 0

    for trialCond in training:

        ti += 1 
        total = training.nTotal
        trialInfo,corrCount = trial.runTrial(win,trialCond,ti,total,corrCount,isTrain=True)

        training.data.add('targets',trialInfo['targets'])
        training.data.add('response',trialInfo['response'])
        training.data.add('results',trialInfo['results'])

        exp.nextEntry() # what's the difference from trialhandler next()

    if corrCount < trainThre:
        expInstructions.train_again(win)
    else:
        expInstructions.train_pass(win)

training.saveAsText(fileName=trainDataFile,stimOut=['tarDir'],dataOut=['targets_raw','response_raw','results_raw'])
training.saveAsPickle(fileName=trainDataFile)



#####################################################
# task session 
#####################################################

# TODO:
# 1. add a new instruction, have 3 sessions, each have 4 blocks, each 40 trials
# 2. if spacondition = all, make trial dict list 3 times, each with different 

expInstructions.task_Instruction_3spa(win,trialNum,taskBlockLen)


if spaCond == 'all':
    spaCond_list = ['HRTF','ITD','ILD']
    trialNum_cond = int(trialNum/len(spaCond_list))

    for s in spaCond_list:

        # make dict list
        taskConds = makeTrialDictList.makeTrialDictList(spaCond=s,isTrain=False,trialNum=trialNum_cond,interruptRatio=ratio,intDir=expInfo['Condition']) 
        tasks = data.TrialHandler(trialList=taskConds, nReps=1, name='task_'+s, method='random') 
        exp.addLoop(tasks)

        # trial handler

        ti = 0
        corrCount = 0

        for taskCond in tasks: 

            if ti % taskSessionLen == 0:
                session_next = int(ti/taskSessionLen)+1
                expInstructions.start_session(win,session_next)

            if ti % taskBlockLen == 0:
                block_next = int(ti/taskBlockLen)+1
                expInstructions.start_block(win,block_next)

            ti += 1
            total = tasks.nTotal
            trialInfo,corrCount = trial.runTrial(win,taskCond,ti,total,corrCount=corrCount,isTrain=False)

            tasks.data.add('targets',trialInfo['targets'])
            tasks.data.add('response',trialInfo['response'])
            tasks.data.add('results',trialInfo['results'])
            tasks.data.add('corrCount',corrCount)

            if ti % taskBlockLen == 0:
                blocki = int(ti/taskBlockLen)
                expInstructions.task_break(win,blocki)
            
            exp.nextEntry()

        tasks.saveAsText(fileName=taskDataFile,stimOut=['spaCond','tarDir','intCond'],dataOut=['targets_raw','response_raw','results_raw','corrCount_raw'])
        tasks.saveAsPickle(fileName=taskDataFile)

else: # spaCond is one spaCond

    taskConds = makeTrialDictList.makeTrialDictList(spaCond=spaCond,isTrain=False,trialNum=trialNum,interruptRatio=ratio,intDir=expInfo['Condition']) 
    tasks = data.TrialHandler(trialList=taskConds, nReps=1, name='task', method='random') 
    exp.addLoop(tasks)

    ti = 0
    corrCount = 0
    for taskCond in tasks: 

        ti += 1
        total = tasks.nTotal
        trialInfo,corrCount = trial.runTrial(win,taskCond,ti,total,corrCount=corrCount,isTrain=False)

        tasks.data.add('targets',trialInfo['targets'])
        tasks.data.add('response',trialInfo['response'])
        tasks.data.add('results',trialInfo['results'])
        tasks.data.add('corrCount',corrCount)

        if ti % taskBlockLen == 0:
            blocki = int(ti/taskBlockLen)
            expInstructions.task_break(win,blocki)
        
        exp.nextEntry()

    tasks.saveAsText(fileName=taskDataFile,stimOut=['spaCond','tarDir','intCond'],dataOut=['targets_raw','response_raw','results_raw','corrCount_raw'])
    tasks.saveAsPickle(fileName=taskDataFile)


# TODO: what's the difference between experiment handler saving and trial handler saving?
exp.saveAsPickle(fileName=expDataFile)
exp.saveAsWideText(fileName=expDataFile)

#port.close()
sys.exit(0)


