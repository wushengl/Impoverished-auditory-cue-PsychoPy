from psychopy import visual, core, event


def showInstruction(win):

    inst_s1 = 'In this task you will first hear an auditory cue ("ba") coming from either the left or right. '\
        'After a short silence, three syllables will play from the left, and three from the right, overlapping in time.  '\
        'Each of the syllables can be either "ba", "da", or "ga".\n\n'\
        'Press Space to move on.'
    inst_s2 = 'You should focus on the syllables from the side indicated by the auditory cue, ignoring the syllables on the other side. \n'\
        'After the end of the sounds, you’ll be asked to click on the screen to indicate the syllables that played from the cued side.\n'\
        'Please try to stare at the fixation cross in the center of the screen and stay still while listening.\n\n'\
        'Press Space to move on.'

    instructions = [inst_s1,inst_s2]

    for s in instructions:
        text = visual.TextStim(win, text=s, alignText='left',height=0.08) 
        text.draw()
        win.flip()
        event.waitKeys(keyList=['space']) 


def train_playExample(win):
    # maybe don't need this screen
    # 1. add sample sound  
    # 2. press 'r' to repeat, press 'space' to move on (button is not as easy as keyboard, but can we use keyboard in booth?)
    # 3. change the text for the target stream (can still play a pregenerated stream here)
    txt = 'Click the play button below to play an example. \n'\
        'In this example, the auditory cue ("ba") is coming from left, so your target stream is coming from left. '\
        'The target stream is "ba", ''ga", "da" in this example.\n'\
        'You can play the example a few more times by pressing R.\n'\
        'Press Space to move on.'
    
    text = visual.TextStim(win, text=txt, alignText='left') 
    text.draw()
    win.flip()
    event.waitKeys(keyList=['space']) 


def train_critInstruction(win):
    # 'if you failed to pass the training 5 times, you will not be able to participate in this experiment.\n'\

    txt = 'Next you will practice with 6 trials, each audio will be played only once.\n'\
        'You need to have at least 4 correct out of 6 trials to pass the training session and move on to the task.\n\n'\
        'Press Space to start the training.'

    text = visual.TextStim(win, text=txt, alignText='left',height=0.08) 
    text.draw()
    win.flip()
    event.waitKeys(keyList=['space'])

def train_again(win):
    txt = 'You didn\'t pass the training session. Please try again or ask for help. \n\n'\
        'Press Space to start the task Session.'

    txt = visual.TextStim(win, text=txt)
    txt.draw()
    win.flip()
    event.waitKeys(keyList=['space'])
    

def train_pass(win):
    txt = 'Congratulations!! You have passed the training session. \n\n'\
        'Press Space to start the task Session.' 

    txt = visual.TextStim(win, text=txt)
    txt.draw()
    win.flip()
    event.waitKeys(keyList=['space'])

def task_Instruction(win,trialNum,taskBlockLen):

    N = int(trialNum/taskBlockLen)

    txt = 'Next you will start the task session. There will be '+str(trialNum)+' trials in total,'\
        ' devided into '+str(N)+' blocks, each block has '+ str(taskBlockLen)+' trials. \n\n'\
        'Press Space to start the task Session.' 

    txt = visual.TextStim(win, text=txt, alignText='left')
    txt.draw()
    win.flip()
    event.waitKeys(keyList=['space'])

def task_break(win,blocki):

    txt = 'You have finished block ' + str(blocki) + '! \n'\
        'Take a break if you need to. \n\n'\
        'Press Space to start the task Session.'

    txt = visual.TextStim(win, text=txt)
    txt.draw()
    win.flip()
    event.waitKeys(keyList=['space'])


