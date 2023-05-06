import json
import unittest

import azure.functions as func

from onedrive_file_processor import main


class TestFunction(unittest.TestCase):
    
    def test_no_params(self):
        req = func.HttpRequest(
            method='POST',
            body=b'{}',
            url='/api/onedrive_file_processor'
        )
        resp = main(req)
        self.assertEqual(resp.status_code, 200)
        
    def test_multitple_audio(self):
        audio = [
            {
            "fileLink": "https://1drv.ms/u/s!AtXdrMCFZ47igcl8Ox8oc3OAc71JZA",
            "path": "/class_recordings/itakello_en/Test/Test-en - Copy.m4a"
            },
            {
            "fileLink": "https://1drv.ms/u/s!AtXdrMCFZ47igcl95UePK8v-15RPBQ",
            "path": "/class_recordings/itakello_en/Test/Test-en - Copy (2).m4a"
            },
            {
            "fileLink": "https://1drv.ms/u/s!AtXdrMCFZ47igcl-xv_c5E_4NDOx8A",
            "path": "/class_recordings/itakello_en/Test/Test-en - Copy (3).m4a"
            }
        ]
        body = json.dumps({"audio": audio}).encode()
        req = func.HttpRequest(
            method='POST',
            body=body,
            url='/api/onedrive_file_processor'
        )
        resp = main(req)
        self.assertEqual(resp.status_code, 200)
    
    def test_multitple_audio_partial_path(self):
        audio = [
            {
            "fileLink": "https://1drv.ms/u/s!AtXdrMCFZ47igcl8Ox8oc3OAc71JZA",
            "path": "itakello_en/Test/Test-en - Copy.m4a"
            },
            {
            "fileLink": "https://1drv.ms/u/s!AtXdrMCFZ47igcl95UePK8v-15RPBQ",
            "path": "itakello_en/Test/Test-en - Copy (2).m4a"
            },
            {
            "fileLink": "https://1drv.ms/u/s!AtXdrMCFZ47igcl-xv_c5E_4NDOx8A",
            "path": "itakello_en/Test/Test-en - Copy (3).m4a"
            }
        ]
        body = json.dumps({"audio": audio}).encode()
        req = func.HttpRequest(
            method='POST',
            body=body,
            url='/api/onedrive_file_processor'
        )
        resp = main(req)
        self.assertEqual(resp.status_code, 200)
    
    def test_zero_audio(self):
        body = json.dumps({"audio": []}).encode()
        req = func.HttpRequest(
            method='POST',
            body=body,
            url='/api/onedrive_file_processor'
        )
        resp = main(req)
        self.assertEqual(resp.status_code, 200)