from unittest import TestCase
from net.wyun.mer.ink.sample import Sample

import numpy as np
import MySQLdb
import _mysql

'''
test mysql db
'''


class TestEquation(TestCase):
    def setUp(self):
        # Open database connection

        self.db = MySQLdb.connect("host6", 3308, "uxb", "uxb123", "uxb", charset = 'utf8',use_unicode=True)

    # ending the test
    def tearDown(self):
        """Cleaning up after the test"""
        print "\nTest:tearDown_:begin"
        # disconnect from server
        self.db.close()


    def test_mysql(self):
        '''
        test fancy index
        array of indices on the matrix
        used a lot in 2-D matrix value update
        :return:
        '''

        # prepare a cursor object using cursor() method
        cursor = self.db.cursor()

        sql = "select id, scg_ink from hw_record where request_at like '2018-09-17%' order by request_at asc;"

        cnt = 0
        try:
            # Execute the SQL command
            #    id | bigint(20) | NO | PRI | NULL | auto_increment |
            # | create_t | datetime | NO | | NULL | |
            # | image_name | varchar(255) | NO | | NULL | |
            # | latex | varchar(255) | NO | | NULL | |
            # | verified | bit(1) | YES | | NULL | |
            # | file_name
            cursor.execute(sql)
            # Fetch all the rows in a list of lists.
            results = cursor.fetchall()
            print 'total records: ', len(results)
            for row in results:
                cnt = cnt +1
                id, scg = row[0], row[1]
                #print 'type of verified: ', type(verified)
                # Now print fetched result
                print 'saving scg... ', id
                self.save_scg_2_file(cnt, scg)
                #if cnt>10: break

        except:
            print "Error: unable to fecth data"
            raise

        print 'total records: ', len(results)


    def save_scg_2_file(self, i, scg):
        textfile = open('temp/2017-09-17/' + str(i) + '_scg.txt', 'w')
        textfile.write(scg)
        textfile.close()