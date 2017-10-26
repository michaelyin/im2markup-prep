# separate a folder into train,validate and test set and dump thus into three file
from __future__ import division
from random import shuffle
import pickle
import fnmatch
import os
import codecs
from net.wyun.mer.ink.sample import Sample
from os.path import basename
from scipy import misc

'''
   from a folder contains inkml files (files ending with .inkml), generate 3 list
   one for dev, one for training, and one for validate. the program will get inkml files
   recursively.
   the *.flist file is an pickle file which contains list of file names (absolute path version)

   usage: test_batch.py for more information
'''


class Batch(object):
    def __init__(self, file_path, list_out_dir='data/batch/pickle/'):
        '''

        :param file_path: directory contains *.inkml files
        :param list_out_dir: 3 list would be generated, one for training, one for test, and the other validation
        '''
        self.inkml_file_path = os.path.realpath(file_path)  # absolute path
        self.list_out_dir = list_out_dir
        self.latex_index = 0

    def generate_lists(self):
        '''
        retrieve all inkml files in self.inkml_file_path, check if it has latex truth information. if yes, add it to
        a list files. divide files into 3 categories. One for training, one for test, and the other validate. the share
        is in 80:10:10.
        :return:
        '''
        files = []
        for root, dirnames, filenames in os.walk(self.inkml_file_path, followlinks=True):
            for filename in fnmatch.filter(filenames, '*.inkml'):
                tmp_path = os.path.join(root, filename)
                #print tmp_path
                sample = Sample(tmp_path)
                if hasattr(sample, 'latex'):
                    #print 'latex: ', tmp_path
                    files.append(tmp_path)

        shuffle(files)
        print 'total files: ', len(files)

        total = len(files)
        validate_num = int(total * 10 / 100)
        test_num = validate_num

        print 'validate num: ', validate_num
        validate = files[:validate_num]

        test = files[validate_num:validate_num + test_num]
        train = files[validate_num + test_num:]

        print 'test num: ', len(test)
        print 'train num: ', len(train)

        list_out_dir = self.list_out_dir
        with open(list_out_dir + 'validate.flist', 'wb') as fout:
            pickle.dump(validate, fout)

        with open(list_out_dir + 'test.flist', 'wb') as fout:
            pickle.dump(test, fout)

        with open(list_out_dir + 'train.flist', 'wb') as fout:
            pickle.dump(train, fout)

        with open(list_out_dir + 'total.flist', 'wb') as fout:
            pickle.dump(files, fout)

    def process_flist(self, infile, outfile, latex_out):
        '''

        :param infile: for example, data/batch/pickle/train.flist
        :param outfile: for example, data/batch/train.lst
        :param latex_out: 'data/batch/latex_list.txt'
        :return:
        '''
        print 'input: ', infile
        print 'output: ', outfile

        with open(infile, 'rb') as fin:
            flist = pickle.load(fin)

        png_dir = 'data/batch/images/'
        with codecs.open(outfile, 'w', 'utf-8') as f_out:
            for file_path in flist:
                print 'file: ', file_path
                # process one file
                sample = Sample(file_path)
                latex = sample.latex
                #output latex
                latex_out.write(latex[1:-1] + '\n')
                #get filename without extension
                png_name = self.get_filename_noext(file_path)
                line = str(self.latex_index) + ' ' + png_name + ' ' + 'basic\n'
                f_out.write(line)
                #output image
                img, W, H = sample.render()
                misc.imsave(png_dir + png_name + '.png', img)
                self.latex_index += 1

    def get_filename_noext(self, file_path):
        # now you can call it directly with basename
        base = basename(file_path)
        return os.path.splitext(base)[0]

    def generate_im2markup_files(self):
        '''
        process train.flist, test.flist, and validate.flist
        produce train.lst, test.lst, and validate.lst
        :return:
        '''
        #with open("latex_list.txt", "w") as f:
        with codecs.open('data/batch/latex_list.txt', 'w', 'utf-8') as latex_out:
            #line = str(mydict[s]) + ' ' + s[0] + ' ' + str(s[1])
            #       fout.write(line + '\n')
            print "No dir specified, using default dir"
            base_dir = 'data/batch/' #self.list_out_dir
            flist_base_dir = self.list_out_dir
            pair_file_name = 'train'
            print 'generate ', pair_file_name, ' lst'
            self.process_flist(flist_base_dir + pair_file_name + '.flist', base_dir + pair_file_name + '.lst', latex_out)
            pair_file_name = 'validate'
            print 'generate ', pair_file_name, ' lst'
            self.process_flist(flist_base_dir + pair_file_name + '.flist', base_dir + pair_file_name + '.lst', latex_out)
            pair_file_name = 'test'
            print 'generate ', pair_file_name, ' lst'
            self.process_flist(flist_base_dir + pair_file_name + '.flist', base_dir + pair_file_name + '.lst', latex_out)

