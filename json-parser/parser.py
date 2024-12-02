from enum import Enum
from sys import argv
from typing import List


def parse_json_file(file_path: str):
    try:
        with open(file_path, "r") as file:
            contents = file.read()
            return parse_json(contents)
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)


def parse_json(json_string):
    """Parses a JSON string and returns a dictionary
    :param json_string: A string containing JSON data
    :return: A dictionary containing the JSON data
    """
    raw_json = json_string.strip()
    if len(raw_json) == 0:
        raise ValueError("The JSON string is empty.")
    token_list = tokenize_json(raw_json)
    return parse_tokens(token_list)


class TokenType(Enum):
    LEFT_BRACE = "{"
    RIGHT_BRACE = "}"
    LEFT_BRACKET = "["
    RIGHT_BRACKET = "]"
    COLON = ":"
    COMMA = ","
    STRING = "STRING"


class JSONToken:
    def __init__(self, token_type: TokenType, value: str):
        self.token_type = token_type
        self.value = value

    def __str__(self):
        return f"Token({self.token_type}, {self.value})"

    def __repr__(self):
        return self.__str__()


def tokenize_json(json_string):
    tokens = []
    idx = 0
    while idx < len(json_string):
        char = json_string[idx]
        if char == "{":
            tokens.append(JSONToken(TokenType.LEFT_BRACE, char))
        elif char == "}":
            tokens.append(JSONToken(TokenType.RIGHT_BRACE, char))
        elif char == "[":
            tokens.append(JSONToken(TokenType.LEFT_BRACKET, char))
        elif char == "]":
            tokens.append(JSONToken(TokenType.RIGHT_BRACKET, char))
        elif char == ":":
            tokens.append(JSONToken(TokenType.COLON, char))
        elif char == ",":
            tokens.append(JSONToken(TokenType.COMMA, char))
        elif char == '"':
            end_idx = json_string.find('"', idx + 1)
            tokens.append(JSONToken(TokenType.STRING, json_string[idx + 1 : end_idx]))
            idx = end_idx
        idx += 1
    return tokens


def parse_tokens(tokens: List[JSONToken]):
    idx = 0
    obj = None
    while idx < len(tokens):
        token = tokens[idx]
        if token.token_type == TokenType.LEFT_BRACE:
            [obj, end_idx] = parse_object(tokens[idx + 1 :])
            idx = end_idx + 1
        idx += 1
    return obj


def parse_object(tokens: List[JSONToken]):
    obj = {}
    key = None
    valid_next_tokens = [TokenType.STRING, TokenType.RIGHT_BRACE]
    idx = 0
    while idx < len(tokens):
        token = tokens[idx]
        if token.token_type not in valid_next_tokens:
            raise ValueError(f"Invalid token: {token}")
        if token.token_type == TokenType.RIGHT_BRACE:
            return [obj, idx]
        elif token.token_type == TokenType.STRING:
            if key is None:
                key = token.value
                valid_next_tokens = [TokenType.COLON]
            else:
                obj[key] = token.value
                key = None
                valid_next_tokens = [TokenType.COMMA, TokenType.RIGHT_BRACE]
        elif token.token_type == TokenType.COLON:
            valid_next_tokens = [TokenType.STRING]
        elif token.token_type == TokenType.COMMA:
            valid_next_tokens = [TokenType.STRING]
        idx += 1
    return [obj, idx]


def main():
    if len(argv) < 2:
        file_path = input("Enter the path to the file: ")
    else:
        file_path = argv[1]
    json_dict = parse_json_file(file_path)
    if json_dict:
        print(json_dict)


if __name__ == "__main__":
    main()
