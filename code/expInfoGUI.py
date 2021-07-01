from psychopy import gui
from psychopy import __version__

# create symbolic link for the 2 files, to solve problem of couldn't find libxcb-util.so
# sudo ln /usr/lib/x86_64-linux-gnu/libxcb-util.so.0.0.0 /usr/lib/x86_64-linux-gnu/libxcb-util.so.1

def showGUI(condition,spatialization,trialNum=96,blockNum=2):

    info = {'Condition':condition,
        'Spatialization':spatialization,
        'Subject': '001',
        'Trial Number': trialNum, 
        'Block Number': blockNum,
        'PsychoPy Version': __version__}

    # Use this dict to create the dlg
    infoDlg = gui.DlgFromDict(dictionary=info, 
        title='Auditory Spatial Attention',
        order=['Condition','Spatialization','Subject','Trial Number','Block Number','PsychoPy Version'],
        fixed=['PsychoPy Version'])  

    if infoDlg.OK: 
        print(info)
    else: 
        print('User Cancelled')

    return info

## You could also use a gui.Dlg and you manually extract the data, this approach gives more 
## control, eg, text color.

'''
# Create dlg
dlg = gui.Dlg(title="Auditory Spatial Attention", pos=(200, 400))
# Add each field manually
dlg.addText('Subject Info', color='Blue')
dlg.addField('ID:', tip='or subject code')
dlg.addField('Other:', '')
dlg.addText('Experiment Info', color='Blue')
dlg.addField('', 45)
# Call show() to show the dlg and wait for it to close (this was automatic with DlgFromDict
thisInfo = dlg.show()

if dlg.OK: # This will be True if user hit OK...
    print(thisInfo)
else:
    print('User cancelled') # ...or False, if they hit Cancel
'''
