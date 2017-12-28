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
from xlsx import Excel
from net.wyun.mer.ink.scg import Scg


'''
   from a folder contains inkml files (files ending with .inkml), generate 3 list
   one for dev, one for training, and one for validate. the program will get inkml files
   recursively.
   the *.flist file is an pickle file which contains list of file names (absolute path version)

   usage: test_batch.py for more information
'''

import logging
logger= logging.getLogger("batch")
logging.basicConfig(format='%(asctime)s - %(funcName)s - %(message)s', filename='temp/batch.log',level=logging.DEBUG)


png_dir = 'data/batch/formula_images/'
class Batch(object):
    def __init__(self, inkml_file_path, xlsx_file_path, list_out_dir='data/batch/pickle/'):
        '''

        :param inkml_file_path: directory contains *.inkml files
        :param list_out_dir: 3 list would be generated, one for training, one for test, and the other validation
        '''
        self.inkml_file_path = os.path.realpath(inkml_file_path)  # absolute path
        self.xlsx_file_path = os.path.realpath(xlsx_file_path)
        self.list_out_dir = list_out_dir
        self.latex_index = 0
        self.latex_length_threshold = 6 # if length < 4, this inkml file is not included
        #self.scgs = self.load_all_scgs()
        self.id_blacklist = self.blacklist()

    def blacklist(self):
        l = []
        l.append(1509259382091)
        l.append(1509239879109)
        return l


    def generate_scg_idlists(self):
        '''
        handle xlsx files
        from a list of xlsx files, generate three scg list: train, validate, and test.
        it store the ids for scg files embedded in the excel files
        :return:
        '''
        ids = list(self.scgs.keys())
        ids_2nd = []

        for id in ids:
            if id in self.id_blacklist:
                continue

            scg = self.scgs[id]
            if scg.get_latex() == '1' or scg.get_latex() == 'i':
                continue

            aspect = scg.w_h_ratio
            if aspect > 80.0 or aspect < 0.02: #scg.get_latex() == '1':
                print '==========> scg aspect: ', aspect
                continue
            scg.save_image('data/batch/formula_images/' + str(id) + '.png')
            ids_2nd.append(id)
        ids = ids_2nd

        shuffle(ids)
        print 'total ids: ', len(ids)

        total = len(ids)
        validate_num = int(total * 10 / 100)
        test_num = validate_num

        print 'validate num(ids): ', validate_num
        validate = ids[:validate_num]

        test = ids[validate_num:validate_num + test_num]
        train = ids[validate_num + test_num:]

        print 'test num(ids): ', len(test)
        print 'train num(ids): ', len(train)

        list_out_dir = self.list_out_dir
        with open(list_out_dir + 'validate.idlist', 'wb') as fout:
            pickle.dump(validate, fout)

        with open(list_out_dir + 'test.idlist', 'wb') as fout:
            pickle.dump(test, fout)

        with open(list_out_dir + 'train.idlist', 'wb') as fout:
            pickle.dump(train, fout)

        with open(list_out_dir + 'total.idlist', 'wb') as fout:
            pickle.dump(ids, fout)

    def load_all_scgs(self):
        '''
        From a list of .xlsx files, generate a dictionary of Scgs with key is the id of Scg
        :return: scgs, dictionary of Scgs
        '''
        scgs = {}  # dictionary of Scgs
        aspect_ratios = {}
        with codecs.open('data/invalid_scgs.txt', 'w', 'utf-8') as f_out:
            for root, dirnames, filenames in os.walk(self.xlsx_file_path, followlinks=True):
                for filename in fnmatch.filter(filenames, '*.xlsx'):
                    tmp_path = os.path.join(root, filename)
                    # print tmp_path
                    excel = Excel(tmp_path)
                    max_row = excel.get_row_number()
                    for idx in range(1, max_row):
                        print idx
                        id, scg, truth, req_at, resp_at = excel.get_scg_record(idx)
                        if len(truth.strip()) == 0:
                            print id
                            line = str(id) + ' ' + 'no latex\n'
                            f_out.write(line)
                            continue
                        scgs[id] = Scg(id, scg, truth, req_at, resp_at)
                        aspect_ratios[id] = scgs[id].w_h_ratio
        #dump aspect_ratios to a file
        ars = aspect_ratios.values()
        print 'aspect ratio min, mean, max: ', min(ars), max(ars), sum(ars) / float(len(ars))

        with open(self.list_out_dir + 'aspectratio.dict', 'wb') as fout:
            pickle.dump(aspect_ratios, fout)
        return scgs

    def all_inkml_files(self):
        '''

        :return: files, files_nolatex
        '''
        files = []
        files_nolatex = []
        for root, dirnames, filenames in os.walk(self.inkml_file_path, followlinks=True):
                for filename in fnmatch.filter(filenames, '*.inkml'):
                    tmp_path = os.path.join(root, filename)
                    print tmp_path
                    sample = Sample(tmp_path)
                    if hasattr(sample, 'latex') and self.check_latex_length(sample):  #latex has been stripped
                        #print 'latex: ', tmp_path

                        files.append(tmp_path)
                    else:
                        files_nolatex.append(tmp_path)
        return files, files_nolatex

    def generate_filelists(self):
        '''
        retrieve all inkml files in self.inkml_file_path, check if it has latex truth information. if yes, add it to
        a list files. divide files into 3 categories. One for training, one for test, and the other validate. the share
        is in 80:10:10.
        :return:
        '''
        files, files_nolatex = self.all_inkml_files()

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
        print 'files w/o latex num: ', len(files_nolatex)

        list_out_dir = self.list_out_dir
        with open(list_out_dir + 'validate.flist', 'wb') as fout:
            pickle.dump(validate, fout)

        with open(list_out_dir + 'test.flist', 'wb') as fout:
            pickle.dump(test, fout)

        with open(list_out_dir + 'train.flist', 'wb') as fout:
            pickle.dump(train, fout)

        with open(list_out_dir + 'total.flist', 'wb') as fout:
            pickle.dump(files, fout)

        with open(list_out_dir + 'nolatex.flist', 'wb') as fout:
            pickle.dump(files_nolatex, fout)

    def check_latex_length(self, sample):
        return True
        #return len(sample.latex) >= self.latex_length_threshold

    def process_list(self, pair_file_name, latex_out):
        '''

        :param pair_file_name, set name: for example, 'train', one train.flist, the other train.idlist
        :param outfile: for example, data/batch/train.lst
        :param latex_out: 'data/batch/latex_list.txt'
        :return:
        '''
        print "No dir specified, using default dir"
        base_dir = 'data/batch/'  # self.list_out_dir
        flist_base_dir = self.list_out_dir
        prefix = 'im2latex_'

        infile = flist_base_dir + pair_file_name + '.flist'     # data/batch/pickle/train.flist
        outfile = base_dir + prefix + pair_file_name + '.lst'   # data/batch/im2latex_train.lst
        scg_id_list_file = flist_base_dir + pair_file_name + '.idlist'

        print 'input: ', infile
        print 'output: ', outfile

        with open(infile, 'rb') as fin:
            flist = pickle.load(fin)

        with open(scg_id_list_file, 'rb') as fin:
            idlist = pickle.load(fin)

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
            for id in idlist:
                print 'id: ', id
                logging.info('processing %d scg record', id)
                scg = self.scgs[id]
                latex = scg.get_latex()
                # output latex
                latex_out.write(latex + '\n')
                # get filename without extension
                png_name = str(id)
                line = str(self.latex_index) + ' ' + png_name + ' ' + 'basic\n'
                f_out.write(line)
                # output image (this task is done when dividing the list into 3 groups
                #scg.save_image(png_dir + png_name + '.png')
                self.latex_index += 1

    def get_filename_noext(self, file_path):
        # now you can call it directly with basename
        base = basename(file_path)
        return os.path.splitext(base)[0]

    # This function is deprecated. Now all im2markup files would be generated based on database equation table
    def generate_im2markup_files(self):
        '''
        process train.flist, test.flist, and validate.flist
        produce train.lst, test.lst, and validate.lst
        :return:
        '''
        #with open("latex_list.txt", "w") as f:
        with codecs.open('data/batch/im2latex_formulas.lst', 'w', 'utf-8') as latex_out:
            #line = str(mydict[s]) + ' ' + s[0] + ' ' + str(s[1])
            #       fout.write(line + '\n')
            print "No dir specified, using default dir"
            base_dir = 'data/batch/' #self.list_out_dir
            flist_base_dir = self.list_out_dir
            prefix = 'im2latex_'
            pair_file_name = 'train'
            print 'generate ', pair_file_name, ' lst'
            self.process_list(pair_file_name, latex_out)
            pair_file_name = 'validate'
            print 'generate ', pair_file_name, ' lst'
            self.process_list(pair_file_name, latex_out)
            pair_file_name = 'test'
            print 'generate ', pair_file_name, ' lst'
            self.process_list(pair_file_name, latex_out)

    def inkml2png(self):
        '''
        for all inkml files in data/batch/inkml folder, generate its png image and save it
        to data/batch/formula_images/ folder

        It is used if different resolution images need to be generated for mhr performance evaluation.
        :return:
        '''
        files, files_nolatex = self.all_inkml_files()
        for file_path in files:
            print 'file: ', file_path
            # process one file
            sample = Sample(file_path)
            # get filename without extension
            png_name = self.get_filename_noext(file_path)
            # output image
            img, W, H = sample.render()
            misc.imsave(png_dir + png_name + '.png', img)
