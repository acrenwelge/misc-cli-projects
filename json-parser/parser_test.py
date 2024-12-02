import json
import unittest
from parser import parse_json_file


class TestJsonParser(unittest.TestCase):

    def setUp(self):
        basepath = "./test-data"
        self.test_data = {
            "step1": {
                "valid": [f"{basepath}/step1/valid.json"],
                "invalid": [f"{basepath}/step1/invalid.json"],
            },
            "step2": {
                "valid": [
                    f"{basepath}/step2/valid.json",
                    f"{basepath}/step2/valid2.json",
                ],
                "invalid": [
                    f"{basepath}/step2/invalid.json",
                    f"{basepath}/step2/invalid2.json",
                ],
            },
            "step3": {
                "valid": [f"{basepath}/step3/valid.json"],
                "invalid": [f"{basepath}/step3/invalid.json"],
            },
            "step4": {
                "valid": [
                    f"{basepath}/step4/valid.json",
                    f"{basepath}/step4/valid2.json",
                ],
                "invalid": [f"{basepath}/invalid.json"],
            },
        }

    def test_step_1_valid(self):
        filepaths = self.test_data["step1"]["valid"]
        for fp in filepaths:
            with open(fp, "r") as file:
                data = json.load(file)
                self.assertEqual(parse_json_file(fp), data)

    def test_step_1_invalid(self):
        filepaths = self.test_data["step1"]["invalid"]
        for fp in filepaths:
            with self.assertRaises(SystemExit) as cm:
                parse_json_file(fp)
            self.assertEqual(cm.exception.code, 1)

    def test_step_2_valid(self):
        filepaths = self.test_data["step2"]["valid"]
        for fp in filepaths:
            with open(fp, "r") as file:
                data = json.load(file)
                self.assertEqual(parse_json_file(fp), data)

    def test_step_2_invalid(self):
        filepaths = self.test_data["step2"]["invalid"]
        for fp in filepaths:
            with self.assertRaises(SystemExit) as cm:
                parse_json_file(fp)
            self.assertEqual(cm.exception.code, 1)

    def test_step_3_valid(self):
        filepaths = self.test_data["step3"]["valid"]
        for fp in filepaths:
            with open(fp, "r") as file:
                data = json.load(file)
                self.assertEqual(parse_json_file(fp), data)

    def test_step_3_invalid(self):
        filepaths = self.test_data["step3"]["invalid"]
        for fp in filepaths:
            with self.assertRaises(SystemExit) as cm:
                parse_json_file(fp)
            self.assertEqual(cm.exception.code, 1)

    def test_step_4_valid(self):
        filepaths = self.test_data["step4"]["valid"]
        for fp in filepaths:
            with open(fp, "r") as file:
                data = json.load(file)
                self.assertEqual(parse_json_file(fp), data)

    def test_step_4_invalid(self):
        filepaths = self.test_data["step4"]["invalid"]
        for fp in filepaths:
            with self.assertRaises(SystemExit) as cm:
                parse_json_file(fp)
            self.assertEqual(cm.exception.code, 1)


if __name__ == "__main__":
    unittest.main()
