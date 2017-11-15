#from openpyxl import load_workbook
from openpyxl import load_workbook

class Excel(object):

    def __init__(self, file_path = 'data/scg/test.xlsx'):
        # Load in the workbook
        wb = load_workbook(file_path)

        # Get sheet names
        print(wb.get_sheet_names())  # [u'hw_record', u'Sheet1']

        # Get a sheet by name
        self.worksheet = wb.get_sheet_by_name('hw_record')

    def get_scg_record(self, index):
        '''
        get the id, scg_content, and scg truth for record at index
        :param index: row index in the excel sheet
        :return: (id, scg, scg_truth)
        '''
        if index < 2 or index > self.get_row_number():
            raise ValueError(" index is out of range !!!")
        (idx1, idx2, idx3) = ('A' + str(index), 'B' + str(index), 'C' + str(index))
        return self.worksheet[idx1].value, self.worksheet[idx2].value, self.worksheet[idx3].value

    def get_row_number(self):
        return len(self.worksheet['A'])

