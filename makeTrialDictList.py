'''
This script contains functions used for generating trial list. Simply list the conditions, TrialHandler will do the randomization.

TODO:
- where should we add 3 spatialization conditions?
    - the randomization is done by trialhandler, so we don't want to mix all 3 spatialization condtion trials together
    - I'll have 3 sessions, each has 4 blocks of 40 trials
- do we want the target could be either leading or lagging?
'''

import numpy as np 
import pdb 


def makeTrialDictList(spaCond='HRTF',isTrain=False,trialNum=96,interruptRatio=1/4,intDir='cont'):
    '''
    No need to randomize here, since the trail handler can randomize trials.

    Train: 
        - half target left, half target right
    '''

    if isTrain: 

        listL = [{'spaCond':spaCond, 'tarDir':'30L', 'intCond':None}]*int(trialNum/2)
        listR = [{'spaCond':spaCond, 'tarDir':'30R', 'intCond':None}]*int(trialNum/2)

        condList = listL + listR

    else:

        intNum = int(trialNum*interruptRatio)
        normNum = trialNum - intNum

        if intDir == 'both': # task session with both cont and ips interrupter

            int_cont_L = [{'spaCond':spaCond, 'tarDir':'30L', 'intCond':'cont'}]*int(intNum/4)
            int_cont_R = [{'spaCond':spaCond, 'tarDir':'30R', 'intCond':'cont'}]*int(intNum/4)
            int_ips_L = [{'spaCond':spaCond, 'tarDir':'30L', 'intCond':'ips'}]*int(intNum/4)
            int_ips_R = [{'spaCond':spaCond, 'tarDir':'30R', 'intCond':'ips'}]*int(intNum/4)
            norm_L = [{'spaCond':spaCond, 'tarDir':'30L', 'intCond':None}]*int(normNum/2)
            norm_R = [{'spaCond':spaCond, 'tarDir':'30R', 'intCond':None}]*int(normNum/2)

            condList = int_cont_L + int_cont_R + int_ips_L + int_ips_R + norm_L + norm_R

        else: # task session with cont/ips interrupter

            int_L = [{'spaCond':spaCond, 'tarDir':'30L', 'intCond':intDir}]*int(intNum/2)
            int_R = [{'spaCond':spaCond, 'tarDir':'30R', 'intCond':intDir}]*int(intNum/2)
            norm_L = [{'spaCond':spaCond, 'tarDir':'30L', 'intCond':None}]*int(normNum/2)
            norm_R = [{'spaCond':spaCond, 'tarDir':'30R', 'intCond':None}]*int(normNum/2)

            condList = int_L + int_R + norm_L + norm_R
    
    pdb.set_trace()
    return condList


def makeTrialDictList2(trialNum,ratio=1/4,intDir='cont'):

    intNum = int(trialNum*ratio)
    normNum = trialNum - intNum

    hrtf_int_L = [{'spaCond':'HRTF', 'tarDir':'30L', 'intCond':intDir}]*int(intNum/2)
    hrtf_int_R = [{'spaCond':'HRTF', 'tarDir':'30R', 'intCond':intDir}]*int(intNum/2)
    ild_int_L = [{'spaCond':'ILD', 'tarDir':'30L', 'intCond':intDir}]*int(intNum/2)
    ild_int_R = [{'spaCond':'ILD', 'tarDir':'30R', 'intCond':intDir}]*int(intNum/2)
    itd_int_L = [{'spaCond':'ITD', 'tarDir':'30L', 'intCond':intDir}]*int(intNum/2)
    itd_int_R = [{'spaCond':'ITD', 'tarDir':'30R', 'intCond':intDir}]*int(intNum/2)

    condList = hrtf_int_L + hrtf_int_R + ild_int_L + ild_int_R + itd_int_L + ild_int_R

    return condList



makeTrialDictList(isTrain=False)
#makeTrialDictList(trialNum=96)