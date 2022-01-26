from psychopy import data, logging, gui, visual, core, event, monitors 
from psychopy import __version__

import expInfoGUI
import expInstructions
import makeTrialDictList
import trial

import pdb

import serial
import serial.tools.list_ports
import sys

#import medussa 


#pdb.set_trace()
#device = medussa.open_device(16,16,8) # input device, ouput device, channel


'''
ExtraInfo:
    - participant: ID input from GUI
    - interrupter: 'both' or 'cont' or 'ips'


    50 ms 1k hz, hamming peak amplitude 0.3 (just know where it is)
'''


# settings and parameters 

condition = ['cont','ips','both'] # interrupter condition
spatialization = ['all','HRTF','ITD','ILD']

scr = 0


ratio = 1/2
trialNum = 480 #12 # 480 # test with 12,12,4
blockNum = 12 
taskBlockLen = int(trialNum/blockNum)
taskSessionLen = 160 #4 # 480/3 = 160

expInfo = expInfoGUI.showGUI(condition,spatialization,trialNum=trialNum,blockNum=blockNum,scr=scr)
expDataFile = '../data/ASAExp_' + expInfo['Subject'] + '/ASAExp_' + expInfo['Subject']
trainDataFile = expDataFile + '_train'
taskDataFile = expDataFile + '_task'
expDataFile = expDataFile + '_exp'

trialNum = expInfo['Trial Number']
intCond = expInfo['Condition']
spaCond = expInfo['Spatialization']
subject = expInfo['Subject']

trainNum = 6
trainThre = 4 # TODO


'''
# do we still want to use serial port?
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
                extraInfo={'participant':expInfo['Subject'], 'Condition':intCond,'Spatialization':spaCond}, # could add data/responses here if use exphandler
                runtimeInfo=None,
                originPath=None,
                savePickle=False, 
                saveWideText=True, 
                dataFileName=expDataFile) 
# another option of saving experiment handler data is to set savePickle/saveWideText as True, and set the dataFileName to be your file name (without .csv)
# then add exp.close() at the end of the experiment, it will automatically help you save the data
# but this is not optimal, since the default saved data is tsv, separated with tab
# excel can only show csv separated with ',' correctly, and it's very likely we'll want to preview data in excel
# so I'll manually use the method saveWideText to save csv data instead of using default saving


# pyglet not working here, simply using screen=1 is not working
# have to use win.fullScr with true screen size to have it work correctly
mon = monitors.Monitor('testMonitor')
scr_idx = expInfo['Screen Index']
win = visual.Window(monitor=mon,screen=scr_idx,fullscr=False,size=[1920,1080]) # maybe should make win global as well...
win.fullScr = True

# global keys
event.globalKeys.add('escape', func=core.quit)


#####################################################
# train session 
#####################################################

corrCount = 0 

while corrCount < trainThre:

    expInstructions.showInstruction(win)
    expInstructions.train_critInstruction(win)

    trainConds = makeTrialDictList.makeTrialDictList(spaCond='HRTF',isTrain=True,trialNum=trainNum)  # could also try nReps with trialhandler, but it's also ok to customize 
    training = data.TrialHandler(trialList=trainConds, nReps=1, name='train', method='random')  # didn't use seed here since we want each training to be different
    exp.addLoop(training)

    ti = 0
    corrCount = 0

    for trialCond in training:

        ti += 1 
        total = training.nTotal
        trialCond['subject'] = subject # TODO debug
        trialInfo,corrCount = trial.runTrial(win,trialCond,ti,total,corrCount,isTrain=True)

        # addData to trial handler would automatically add to exp handler, since this trial handler is "attached to" the exp handler
        training.addData('targets', trialInfo['targets'])
        training.addData('response',trialInfo['response'])
        training.addData('results',trialInfo['results'])

        exp.nextEntry() # what's the difference from trialhandler next()

    if corrCount < trainThre:
        expInstructions.train_again(win)
    else:
        expInstructions.train_pass(win)

#training.saveAsText(fileName=trainDataFile,stimOut=['tarDir'],dataOut=['targets_raw','response_raw','results_raw']) 
#training.saveAsPickle(fileName=trainDataFile) 


#####################################################
# task session 
#####################################################


expInstructions.task_Instruction_3spa(win,trialNum,taskBlockLen)


if spaCond == 'all':
    spaCond_list = ['HRTF','ITD','ILD']
    trialNum_cond = int(trialNum/len(spaCond_list))

    ti = 0
    corrCount = 0

    for s in spaCond_list:

        # make dict list
        taskConds = makeTrialDictList.makeTrialDictList(spaCond=s,isTrain=False,trialNum=trialNum_cond,interruptRatio=ratio,intDir=expInfo['Condition']) 
        tasks = data.TrialHandler(trialList=taskConds, nReps=1, name='task_'+s, method='random') # condition in taskConds are automatically saved into exp
        
        exp.addLoop(tasks)

        # trial handler

        for taskCond in tasks: 

            if ti % taskSessionLen == 0:
                print('######################################')
                print('STARTING NEW SESSION!')
                print('######################################')
                # pdb.set_trace()  # TODO: can I stop here and resume again? how would the task window behave?
                session_next = int(ti/taskSessionLen)+1
                expInstructions.start_session(win,session_next)

            if ti % taskBlockLen == 0:
                print('==================')
                print('STARTING NEW BLOCK!')
                print('==================')
                block_next = int(ti/taskBlockLen)+1
                expInstructions.start_block(win,block_next)
                
            print('Current trial: ',ti)

            ti += 1
            total = tasks.nTotal
            ti_show = ((ti-1) % taskSessionLen)+1 
            taskCond['subject'] = subject
            trialInfo,corrCount = trial.runTrial(win,taskCond,ti_show,total,corrCount=corrCount,isTrain=False) 

            tasks.addData('targets',trialInfo['targets'])
            tasks.addData('response',trialInfo['response'])
            tasks.addData('results',trialInfo['results'])
            tasks.addData('corrCount',corrCount)

            # to make it easier for R to process (arrays saved can only be read as string like "[0 1 1]")
            tasks.addData('T1', trialInfo['targets'][0])
            tasks.addData('T2', trialInfo['targets'][1])
            tasks.addData('T3', trialInfo['targets'][2])
            tasks.addData('R1', trialInfo['response'][0])
            tasks.addData('R2', trialInfo['response'][1])
            tasks.addData('R3', trialInfo['response'][2])
            tasks.addData('S1', trialInfo['results'][0]) # S stands for score, results is an array
            tasks.addData('S2', trialInfo['results'][1])
            tasks.addData('S3', trialInfo['results'][2])
            

            if ti % taskBlockLen == 0:
                blocki = int(ti/taskBlockLen)
                expInstructions.task_break(win,blocki)
            
            exp.nextEntry()

        #taskDataFile_cond = taskDataFile + '_' + s
        #tasks.saveAsText(fileName=taskDataFile_cond,stimOut=['spaCond','tarDir','intCond'],dataOut=['targets_raw','response_raw','results_raw','corrCount_raw']) 
        #tasks.saveAsPickle(fileName=taskDataFile_cond) 

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

        tasks.addData('targets',trialInfo['targets'])
        tasks.addData('response',trialInfo['response'])
        tasks.addData('results',trialInfo['results'])
        tasks.addData('corrCount',corrCount)

        tasks.addData('T1', trialInfo['targets'][0])
        tasks.addData('T2', trialInfo['targets'][1])
        tasks.addData('T3', trialInfo['targets'][2])
        tasks.addData('R1', trialInfo['response'][0])
        tasks.addData('R2', trialInfo['response'][1])
        tasks.addData('R3', trialInfo['response'][2])
        tasks.addData('S1', trialInfo['results'][0]) # S stands for score, results is an array
        tasks.addData('S2', trialInfo['results'][1])
        tasks.addData('S3', trialInfo['results'][2])

        if ti % taskBlockLen == 0:
            blocki = int(ti/taskBlockLen)
            expInstructions.task_break(win,blocki)
        
        exp.nextEntry()

    #tasks.saveAsText(fileName=taskDataFile,stimOut=['spaCond','tarDir','intCond'],dataOut=['targets_raw','response_raw','results_raw','corrCount_raw']) 
    #tasks.saveAsPickle(fileName=taskDataFile) 


# here save the data for the whole exp just to be safe, normally I'll still use the customized pandas dataframe for data analysis
exp.saveAsWideText(fileName=expDataFile,delim=',') # when setting delim to be ',', the default extention is '.csv', or the default will be '.tsv'


expInstructions.end_task(win)

#port.close()
sys.exit(0) # I don't remember what is this...


