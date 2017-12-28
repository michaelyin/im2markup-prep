#from openpyxl import load_workbook
from openpyxl import load_workbook
import xlrd
import codecs
import os
from net.wyun.mer.ink.scg import Scg
import pickle
from datetime import datetime

class Excel(object):

    def __init__(self, file_path = 'data/scg/test.xlsx'):
        # Load in the workbook
        self.wb = xlrd.open_workbook(file_path, on_demand = True)

        # Get sheet names
        #print(wb.get_sheet_names())  # [u'hw_record', u'Sheet1']

        # Get a sheet by name
        #self.worksheet = wb.get_sheet_by_name('hw_record')
        self.worksheet = self.wb.sheet_by_index(0)
        #self.scgs = self.load_all_scgs()


    def load_all_scgs(self):
        '''
        From a .xlsx file, generate a dictionary of Scgs with key is the id of Scg
        :return: scgs, dictionary of Scgs
        '''
        scgs = {}  # dictionary of Scgs
        aspect_ratios = {}
        with codecs.open('data/invalid_scgs.txt', 'w', 'utf-8') as f_out:
            max_row = self.get_row_number()
            for idx in range(1, max_row):
                print idx
                id, scg, truth, req_at, resp_at  = self.get_scg_record(idx)
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

        with open( 'aspectratio.dict', 'wb') as fout:
            pickle.dump(aspect_ratios, fout)

        self.scgs = scgs
        return scgs

    def get_scg_record(self, index):
        '''
        get the id, scg_content, and scg truth for record at index
        :param index: row index in the excel sheet
        :return: (id, scg, scg_truth)
        '''
        if index < 1 or index > self.get_row_number():
            print 'index: ', index
            raise ValueError(" index is out of range !!!")
        row = index

        return int(self.worksheet.cell_value(row, 0)), self.worksheet.cell_value(row, 1), \
               self.worksheet.cell_value(row, 2), self.read_datetime(row, 3), \
               self.read_datetime(row, 4)

    def get_row_number(self):
        return self.worksheet.nrows

    def read_datetime(self, row, col):
        # return xlrd.xldate.xldate_as_datetime(self.worksheet.cell_value(row, col), 1)
        cell_v = self.worksheet.cell_value(row, col)
        print 'row, ', row, 'datetime, ', cell_v
        if cell_v:
            return datetime(*xlrd.xldate_as_tuple(cell_v, self.wb.datemode))
        else:
            return ''
