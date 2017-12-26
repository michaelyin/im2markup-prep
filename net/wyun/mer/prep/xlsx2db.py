
from net.wyun.mer.ink.scg import Scg
from xlsx import Excel

'''
process data/xlsx/hw_record.xlsx file, and save its record to DB
New data will be available in sql form. And it can be dumped into DB directly
'''

class Excel2DB(object):
    '''
    This class is used to dump the original scg data into a database. Because all these data has been
    verified for its latex output. So the processed flag is set to 1
    '''

    def __init__(self, dbBatch, xlsx_file_path ='data/scg/test.xlsx'):
        self.excel = Excel(xlsx_file_path)
        self.dbBatch = dbBatch

    def saveScg2db(self, scg):
        hw_record = scg.id, scg.content, scg.response, 1, scg.request_at, scg.response_at
        self.dbBatch.insert_hw_record(hw_record)

    def saveRow2db(self, row):
        scg_id, scg_content, truth, req_at, resp_at = self.excel.get_scg_record(row)
        if len(truth.strip()) == 0:
            print '' + str(id) + ' ' + 'no latex\n'
            return
        scg = Scg(scg_id, scg_content, truth, req_at, resp_at)
        self.saveScg2db(scg)
