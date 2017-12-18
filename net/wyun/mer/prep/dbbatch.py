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
   from a db table (equation), generate 3 list
   one for dev, one for training, and one for validate. the program will get inkml files
   recursively.
   the *.flist file is an pickle file which contains list of file names (absolute path version)

   usage: test_batch.py for more information
'''
import MySQLdb

import logging
logger= logging.getLogger("batch")
logging.basicConfig(format='%(asctime)s - %(funcName)s - %(message)s', filename='temp/dbbatch.log',level=logging.DEBUG)

class DBBatch(object):
    def __init__(self, dbhost, dbuser, dbpass, dbname, list_out_dir='data/batch/pickle/'):
        '''

        :param dbhost: directory contains *.inkml files
        :param list_out_dir: 3 list would be generated, one for training, one for test, and the other validation
        '''
        self.dbhost = os.path.realpath(dbhost)  # absolute path
        self.dbuser = os.path.realpath(dbuser)
        self.list_out_dir = list_out_dir
        self.db = MySQLdb.connect(dbhost, dbuser, dbpass, dbname, charset = 'utf8',use_unicode=True) #"hope", "equation")
        self.sql = "SELECT id, create_t, image_name, latex, (verified=B'1') AS verified, file_name FROM equation"
        self.latex_index = 0
        self.equation_dict = dict()

    def __del__(self):
        print 'destruction here, close db.'
        self.db.close()

    def generate_db_idlists(self):
        '''
        from a list of equation records, generate three id list: train, validate, and test.
        it store the id for equation object
        :return:
        '''

        # prepare a cursor object using cursor() method
        cursor = self.db.cursor()

        not_verified_cnt = 0
        with_chinese_cnt = 0
        ids = []

        try:
            cursor.execute(self.sql)
            # Fetch all the rows in a list of lists.
            results = cursor.fetchall()
            print 'total records: ', len(results)
            for row in results:
                id, create_t, image_name, latex, verified, file_name = row[0], row[1], row[2], row[3], row[4], row[5]
                #print 'type of verified: ', type(verified)
                # Now print fetched result
                if verified == 0:
                    logging.warn("unverified equation: id=%d,create_t=%s,latex=%s,verified=%d,file_name=%s" % \
                          (id, create_t, latex, int(verified), file_name))
                    not_verified_cnt += 1
                    continue

                # ignore record with Chinese
                if self.contains_chinese(latex):
                    logging.warn("contains chininese: id=%d, latex = %s", id, latex)
                    with_chinese_cnt += 1
                    continue

                ids.append(id)

        except:
            logging.exception("DB reading exception!!!")
            raise
        print 'not   verified  equations: ', not_verified_cnt
        print 'equations contain Chinese: ', with_chinese_cnt
        print 'total records: ', len(results)


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

        outfile = base_dir + prefix + pair_file_name + '.lst'   # data/batch/im2latex_train.lst
        equ_id_list_file = flist_base_dir + pair_file_name + '.idlist'

        print 'output: ', outfile

        with open(equ_id_list_file, 'rb') as fin:
            idlist = pickle.load(fin)

        #png_dir = 'data/batch/formula_images/'
        with codecs.open(outfile, 'w', 'utf-8') as f_out:
            for id in idlist:
                print 'id: ', id
                logging.info('processing %d equation record', id)
                id, create_t, image_name, latex, verified, file_name = self.equation_dict[id]
                # output latex
                if latex[0] != '$' or latex[-1] != '$':
                    logging.warning('%d equation record with invalid latex', id)

                latex_out.write(latex[1:-1] + '\n')
                # get filename without extension
                png_name = file_name
                line = str(self.latex_index) + ' ' + png_name + ' ' + 'basic\n'
                f_out.write(line)
                self.latex_index += 1


    def generate_im2markup_files(self):
        '''
        process train.flist, test.flist, and validate.flist
        produce train.lst, test.lst, and validate.lst
        :return:
        '''
        #with open("latex_list.txt", "w") as f:
        #generate equation dictionary

        # prepare a cursor object using cursor() method
        cursor = self.db.cursor()

        try:
            cursor.execute(self.sql)
            # Fetch all the rows in a list of lists.
            results = cursor.fetchall()
            print 'total records: ', len(results)
            for row in results:
                #id, create_t, image_name, latex, verified, file_name
                equation_row  = (row[0], row[1], row[2], row[3], row[4], row[5])
                # Now print fetched results not being verified
                id = row[0]
                if row[4] == 0:
                    print "id=%d,create_t=%s,latex=%s,verified=%d,file_name=%s" % \
                          (row[0], row[1], row[2], row[3], row[4], row[5])
                else:
                    self.equation_dict[id] = equation_row
        except:
            logging.exception("DB reading exception!!!")
            raise

        # generate list: train, validate, test
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

    def contains_chinese(self, latex):
        yes = False
        for i in range(len(latex)):
            if latex[i] > u'\u4e000' and latex[i] < u'\u9fff':
                yes = True
                print id, latex[i]

        return yes