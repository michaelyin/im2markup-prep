#from openpyxl import load_workbook
from openpyxl import load_workbook
import xlrd

class Excel(object):

    def __init__(self, file_path = 'data/scg/test.xlsx'):
        # Load in the workbook
        wb = xlrd.open_workbook(file_path, on_demand = True)

        # Get sheet names
        #print(wb.get_sheet_names())  # [u'hw_record', u'Sheet1']

        # Get a sheet by name
        #self.worksheet = wb.get_sheet_by_name('hw_record')
        self.worksheet = wb.sheet_by_index(0)

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

        return int(self.worksheet.cell_value(row, 0)), self.worksheet.cell_value(row, 1), self.worksheet.cell_value(row, 2)

    def get_row_number(self):
        return self.worksheet.nrows

