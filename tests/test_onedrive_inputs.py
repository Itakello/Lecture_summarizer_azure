import unittest

import azure.functions as func

from onedrive_file_processor import main


class TestFunction(unittest.TestCase):
    def test_no_params(self):
        req = func.HttpRequest(
            method='POST',
            body=None,
            url='/api/onedrive_file_processor'
        )
        resp = main(req)
        self.assertEqual(resp.status_code, 200)
    def test_multitple_links(self):
        links = [
            "https://1drv.ms/u/s!AtXdrMCFZ47igcl8Ox8oc3OAc71JZA",
            "https://1drv.ms/u/s!AtXdrMCFZ47igcl95UePK8v-15RPBQ",
            "https://1drv.ms/u/s!AtXdrMCFZ47igcl-xv_c5E_4NDOx8A"
        ]
        req = func.HttpRequest(
            method='POST',
            body={"links": links},
            url='/api/onedrive_file_processor'
        )
        resp = main(req)
        self.assertEqual(resp.status_code, 200)