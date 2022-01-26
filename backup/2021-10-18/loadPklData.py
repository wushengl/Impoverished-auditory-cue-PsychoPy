import pickle


def getPklData(fileName):
    with open(fileName,'wb'):
        pkl_file = pickle.load(fileName)
        # if it's psychopy experiment handler
        # print(pkl_file._getExtraInfo())
        # print(pkl_file._getAllParamNames())
    
    return pkl_file