# this script is used for checking the data being saved

from psychopy.misc import fromFile
# (replace with the file path to your .psydat file)
#fpath = '../data/ASAExp_001/ASAExp_001_train.psydat'
fpath = '../data/ASAExp_001/ASAExp_001_task_HRTF.psydat'
fpath = '../data/ASAExp_001/ASAExp_001_task_ITD.psydat'

psydata = fromFile(fpath)

''''''
# train.psydat is correct
print(psydata.data['targets'])
print(psydata.data['response'])
print(psydata.data['results'])

# task.psydat is not right, since new session will cover old session
# solution1: specify condition name
# solution2: use exp data?

# TODO: test solution1 (already changed), don't foget to delete all existing data or use subject 002

import pdb; pdb.set_trace()

# TODO: psydata.entries = [] now

fpath = '../data/ASAExp_001/ASAExp_001_exp.psydat'
psydata = fromFile(fpath)

for entry in psydata.entries:
    print(entry)

    
    