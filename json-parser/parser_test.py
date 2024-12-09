import json
import os
import unittest
from parser import (
    JSONToken,
    TokenType,
    parse_json_file,
    parse_number_token,
    parse_string_token,
    tokenize_json,
)

# Get the absolute path to the test data directory
test_data_folder_path = os.path.join(os.path.dirname(__file__), "test-data")


class TestJsonParser(unittest.TestCase):

    def test_parse_numbers(self):
        # Test cases
        json_numbers_valid = [
            "0",
            "-0",
            "123",
            "-123",
            "0.123",
            "-0.123",
            "2e+00",
            "-2e-10",
        ]
        json_numbers_invalid = ["02", "-02", "02.5", "012e+1"]
        for json_num in json_numbers_valid:
            num = float(json_num)
            self.assertEqual(parse_number_token(json_num, 0)[0], num)
        for json_num in json_numbers_invalid:
            with self.assertRaises(ValueError):
                parse_number_token(json_num, 0)

    def test_parse_escaped_chars(self):
        res = parse_string_token('"hello\n\\"world\\""', 0)
        self.assertEqual(res[0], 'hello\n"world"')
        res = parse_string_token('"unicode\u20bf"', 0)
        print(res)
        self.assertEqual(res[0], "unicode\u20bf")

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
        tokens = tokenize_json('"hello"')
        self.assertEqual(tokens, [JSONToken(TokenType.STRING, "hello")])
        tokens = tokenize_json("123")
        self.assertEqual(tokens, [JSONToken(TokenType.NUMBER, 123)])
        tokens = tokenize_json("null")
        self.assertEqual(tokens, [JSONToken(TokenType.NULL, None)])

    def test_tokenize_invalid(self):
        with self.assertRaises(ValueError):
            tokenize_json("{'key': 'value'}")

    def test_steps(self):
        for num in range(1, 5):
            stepfolder = f"step{num}"
            folderpath = os.path.join(test_data_folder_path, stepfolder)
            for filename in os.listdir(folderpath):
                filepath = os.path.join(folderpath, filename)
                with self.subTest(testfile=f"{stepfolder}/{filename}"):
                    if filename.startswith("valid"):
                        with open(filepath, "r") as file:
                            data = json.load(file)
                            self.assertEqual(parse_json_file(filepath), data)
                    elif filename.startswith("invalid"):
                        with self.assertRaises(SystemExit) as cm:
                            parse_json_file(filepath)
                        self.assertEqual(cm.exception.code, 1)

    def test_custom(self):
        folderpath = os.path.join(test_data_folder_path, "custom")
        for filename in os.listdir(folderpath):
            filepath = os.path.join(folderpath, filename)
            with self.subTest(testfile=f"custom/{filename}"):
                if filename.startswith("valid"):
                    with open(filepath, "r") as file:
                        data = json.load(file)
                        self.assertEqual(parse_json_file(filepath), data)
                elif filename.startswith("invalid"):
                    with self.assertRaises(SystemExit) as cm:
                        parse_json_file(filepath)
                    self.assertEqual(cm.exception.code, 1)

    def test_full_suite(self):
        folderpath = os.path.join(test_data_folder_path, "full-suite")
        for filename in os.listdir(folderpath):
            filepath = os.path.join(folderpath, filename)
            with self.subTest(testfile=f"full-suite/{filename}"):
                if filename.startswith("valid"):
                    with open(filepath, "r") as file:
                        data = json.load(file)
                        self.assertEqual(parse_json_file(filepath), data)
                elif filename.startswith("invalid"):
                    with self.assertRaises(SystemExit) as cm:
                        parse_json_file(filepath)
                    self.assertEqual(cm.exception.code, 1)


if __name__ == "__main__":
    unittest.main()
