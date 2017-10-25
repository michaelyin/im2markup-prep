#separate a folder into train,dev and test set and dump thus into three file
from __future__ import division
from random import shuffle
from glob import glob
import pickle
from sys import argv
import fnmatch
import os

'''
   from a folder contains inkml files (files ending with .inkml), generate 3 list
   one for dev, one for training, and one for validation test. the program will get inkml files
   recursively.
   the *.flist file is an pickle file which contains list of file names (absolute version)

   usage: python batch.py path_to_inkmls
'''
inkml_file_path = '../data/batch/inkml/'

arguments = argv[1:]
if len(arguments) > 0:
	inkml_file_path = argv[1]
	for ag in arguments:
		print ag

inkml_file_path = os.path.realpath(inkml_file_path)  # absolute path
'''
files = []
for file_path in glob(inkml_file_path + '/*.inkml*'):
		print(file_path)
		files.append(file_path)
'''
files = []
for root, dirnames, filenames in os.walk(inkml_file_path, followlinks=True):
    for filename in fnmatch.filter(filenames, '*.inkml'):
        files.append(os.path.join(root, filename))

shuffle(files)
print 'total files: ', len(files)

total = len(files)
dev_num = int(total * 1/100)
test_num = dev_num * 5

print 'dev num: ', dev_num
dev = files[:dev_num]

test = files[dev_num:dev_num + test_num]
train = files[dev_num + test_num:]

print 'test num: ', len(test)
print 'train num: ', len(train)

list_out_dir = '../data/batch/pickle/'
with open(list_out_dir + 'dev.flist','wb') as fout:
	pickle.dump(dev,fout)

with open(list_out_dir + 'test.flist','wb') as fout:
	pickle.dump(test,fout)

with open(list_out_dir + 'train.flist','wb') as fout:
	pickle.dump(train,fout)

with open(list_out_dir + 'total.flist','wb') as fout:
	pickle.dump(files,fout)
