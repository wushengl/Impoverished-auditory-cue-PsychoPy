'''
This script is used for checking the RMS levels of source signals (in dB).
'''

import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt

import pdb


def getRMS(sig):
    '''
    - sig: 1-d source signal
    '''
    
    rms = np.sqrt(np.sum(sig**2)/len(sig))
    db = 20*np.log10(rms)

    return rms, db


def truncZeros(sig):
    '''
    This function is used for cutting the zeros padded at the end (if applicable).
    - sig: 1-d source signal
    '''

    sig_locs = np.where(sig!=0)
    last_loc = np.max(sig_locs)

    if last_loc < len(sig)-10:
        sig = sig[:last_loc+10]

    return sig


def checkLevels(file_array, folder):
    '''
    - file_array: an array/list containing names of all the files to check
    - folder: folder path containg all those source files
    '''

    db_list = []

    for f in file_array:
        path = folder + f
        sig, fs = sf.read(path)
        sig = truncZeros(sig)
        rms, db = getRMS(sig)
        db_list.append(db)

    db_arr = np.array(db_list)
    db_mean = np.mean(db_arr)

    for dbi in db_arr:
        if dbi > db_mean+1:
            print('High level observed.')
            raise ValueError
        elif dbi < db_mean-1:
            print('Low level observed.')
            raise ValueError
            
    print('Level check done.')
    print('Levels in dB:')
    print(db_arr)

pass



if __name__ == '__main__':

    folder = '../stimuli/sources/'
    files = ['ba_M2.wav','da_M2.wav','ga_M2.wav','meow.wav']

    checkLevels(files,folder)



    


        

    