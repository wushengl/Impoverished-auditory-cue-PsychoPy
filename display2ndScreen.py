'''
This script is used for testing display task on the second screen. 

In Chris' lab, the 2 screens are regarded by the system as one huge screen, with the control screen being screen 1 (left) and chamber screen being screen 2 (right).
Functions provided here:

- print all the monitors 
- print a text on the screen 
- print size of the monitor
- show on specific location of the monitor (right half screen)
'''


from psychopy import visual, monitors, event, core
import pdb


# add global key esc to quit
event.globalKeys.add('escape', func=core.quit)

# monitors.getAllMonitors() 

# initialize display window

#mon = monitors.Monitor('testMonitor')
#win_size = mon.getSizePix() # [1024, 768] when duplicate screen, still [1024, 768] when extend


# the problem is winType. with winType='pyglet', it can never show on 2nd screen
# with 'glfw', it can show on second screen but it's not showing right
# first a stretched screen showed, then a regular shape, and weird blue lines...
# chamber monitor size 120*1080
win = visual.Window(fullscr=False,size=[1920, 1080], screen=1) # maybe should make win global as well...
win.fullScr = True

# display something on the window
text = visual.TextStim(win, text='Hi!', alignText='center') 
text.draw()
win.flip()

core.wait(5.0)

win.close()
core.quit()










