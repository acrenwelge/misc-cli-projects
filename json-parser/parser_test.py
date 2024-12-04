import json
import os
import unittest
from parser import JSONToken, TokenType, parse_json_file, tokenize_json

# Get the absolute path to the test data directory
test_data_folder_path = os.path.join(os.path.dirname(__file__), "test-data")


class TestJsonParser(unittest.TestCase):

    def setUp(self):
        self.test_data = {
            "step1": {
                "valid": [f"{test_data_folder_path}/step1/valid.json"],
                "invalid": [f"{test_data_folder_path}/step1/invalid.json"],
            },
            "step2": {
                "valid": [
                    f"{test_data_folder_path}/step2/valid.json",
                    f"{test_data_folder_path}/step2/valid2.json",
                ],
                "invalid": [
                    f"{test_data_folder_path}/step2/invalid.json",
                    f"{test_data_folder_path}/step2/invalid2.json",
                ],
            },
            "step3": {
                "valid": [f"{test_data_folder_path}/step3/valid.json"],
                "invalid": [f"{test_data_folder_path}/step3/invalid.json"],
            },
            "step4": {
                "valid": [
                    f"{test_data_folder_path}/step4/valid.json",
                    f"{test_data_folder_path}/step4/valid2.json",
                ],
                "invalid": [f"{test_data_folder_path}/step4/invalid.json"],
            },
        }

    def test_tokenize(self):
        tokens = tokenize_json(
            '{"key": "value", "key-n": 101, "key-o": {"inner key": "inner value"}, "key-l": ["list value"]}'
        )
        self.assertEqual(
            tokens,
            [
                JSONToken(TokenType.LEFT_BRACE, "{"),
                JSONToken(TokenType.STRING, "key"),
                JSONToken(TokenType.COLON, ":"),
                JSONToken(TokenType.STRING, "value"),
                JSONToken(TokenType.COMMA, ","),
                JSONToken(TokenType.STRING, "key-n"),
                JSONToken(TokenType.COLON, ":"),
                JSONToken(TokenType.NUMBER, 101),
                JSONToken(TokenType.COMMA, ","),
                JSONToken(TokenType.STRING, "key-o"),
                JSONToken(TokenType.COLON, ":"),
                JSONToken(TokenType.LEFT_BRACE, "{"),
                JSONToken(TokenType.STRING, "inner key"),
                JSONToken(TokenType.COLON, ":"),
                JSONToken(TokenType.STRING, "inner value"),
                JSONToken(TokenType.RIGHT_BRACE, "}"),
                JSONToken(TokenType.COMMA, ","),
                JSONToken(TokenType.STRING, "key-l"),
                JSONToken(TokenType.COLON, ":"),
                JSONToken(TokenType.LEFT_BRACKET, "["),
                JSONToken(TokenType.STRING, "list value"),
                JSONToken(TokenType.RIGHT_BRACKET, "]"),
                JSONToken(TokenType.RIGHT_BRACE, "}"),
            ],
        )

    def test_tokenize_invalid(self):
        with self.assertRaises(ValueError):
            tokenize_json("{'key': 'value'}")

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
