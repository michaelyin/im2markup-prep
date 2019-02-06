from unittest import TestCase
import requests
import json

#curl -H "Content-Type: application/json;charset=UTF-8 " -X POST -d '{"id":90,"asciimath":"", "mathml":"", "latex":"x \\lt y"}' http://host:port/latex_ to_asciimath


class TestBatch(TestCase):

    def setUp(self):
        self.host = '72.93.93.62:8089'

    def test_mathml2latex(self):
        cuda1_host = 'http://' + self.host + '/latex_to_asciimath'

        payload = {"id":90,"asciimath":"", "mathml":"", "latex":"x \\lt y"}
        headers = {'content-type': 'application/json'}
        r = requests.post(cuda1_host, data=json.dumps(payload), headers=headers)
        print '\n' + r.text
        print '\n' + str(r.headers)