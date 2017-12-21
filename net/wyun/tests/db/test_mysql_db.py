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

        self.db = MySQLdb.connect("localhost", "hope", "hope", "equation", charset = 'utf8',use_unicode=True)

    # ending the test
    def tearDown(self):
        """Cleaning up after the test"""
        print "\nTest:tearDown_:begin"
        # disconnect from server
        self.db.close()

    def contains_chi(self, latex):
        yes = False
        for i in range(len(latex)):
            if latex[i] > u'\u4e000' and latex[i] < u'\u9fff':
                yes = True
                print id, latex[i]

        return yes

    def test_mysql(self):
        '''
        test fancy index
        array of indices on the matrix
        used a lot in 2-D matrix value update
        :return:
        '''

        # prepare a cursor object using cursor() method
        cursor = self.db.cursor()

        sql = "SELECT id, create_t, image_name, latex, (verified=B'1') AS verified, file_name FROM equation"

        not_verified_cnt = 0
        with_chinese_cnt = 0
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
                id, create_t, image_name, latex, verified, file_name = row[0], row[1], row[2], row[3], row[4], row[5]
                #print 'type of verified: ', type(verified)
                # Now print fetched result
                if verified == 0:
                    print "id=%d,create_t=%s,latex=%s,verified=%d,file_name=%s" % \
                      (id, create_t, latex, int(verified) , file_name)
                    not_verified_cnt += 1

                if self.contains_chi(latex):
                    print id, latex
                    with_chinese_cnt += 1
        except:
            print "Error: unable to fecth data"
            raise

        print 'total records: ', len(results)
        print 'total not verified: ', not_verified_cnt
        print 'total with chinese: ', with_chinese_cnt


