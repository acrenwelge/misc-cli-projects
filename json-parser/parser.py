import re
from enum import Enum
from sys import argv
from typing import List

debug_level = "DEBUG"


def debug_print(message: str):
    if debug_level == "DEBUG":
        print(message)


def parse_json_file(file_path: str):
    try:
        with open(file_path, "r") as file:
            contents = file.read()
            debug_print("\nParsing JSON file..." + file_path)
            return parse_json(contents)
    except FileNotFoundError:
        debug_print(f"The file {file_path} does not exist.")
    except Exception as e:
        debug_print(f"An error occurred: {e}")
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
    debug_print(token_list)
    return parse_tokens_fsm(token_list)


class ParserState(Enum):
    # START_PARSING = 0
    START_OBJECT = 1
    READ_KEY = 2
    READ_COLON = 3
    READ_VALUE = 4
    READ_COMMA = 5
    END_OBJECT = 5


class TokenType(Enum):
    LEFT_BRACE = "{"
    RIGHT_BRACE = "}"
    LEFT_BRACKET = "["
    RIGHT_BRACKET = "]"
    COLON = ":"
    COMMA = ","
    STRING = "STRING"
    BOOLEAN = "BOOLEAN"
    NUMBER = "NUMBER"
    NULL = "NULL"


class JSONToken:
    def __init__(self, token_type: TokenType, value):
        self.token_type = token_type
        self.value = value

    def __str__(self):
        return f"Token({self.token_type}, {self.value})\n"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, JSONToken):
            return False
        return self.token_type == other.token_type and self.value == other.value


def tokenize_json(json_string) -> List[JSONToken]:
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
            debug_print("comma at " + str(idx))
            tokens.append(JSONToken(TokenType.COMMA, char))
        elif char == '"':
            end_idx = json_string.find('"', idx + 1)
            tokens.append(JSONToken(TokenType.STRING, json_string[idx + 1 : end_idx]))
            idx = end_idx
        elif char == "'":
            raise ValueError("Invalid token '. Strings must use double quotes.")
        elif json_string[idx : idx + 4] == "true":
            tokens.append(JSONToken(TokenType.BOOLEAN, True))
            idx += 3
        elif json_string[idx : idx + 5] == "false":
            tokens.append(JSONToken(TokenType.BOOLEAN, False))
            idx += 4
        elif json_string[idx : idx + 4] == "null":
            tokens.append(JSONToken(TokenType.NULL, None))
            idx += 3
        elif char.isdigit() or char == "-":
            number_regex = re.compile(r"-?\d+(\.\d+)?([eE][-+]?\d+)?")
            match = number_regex.match(json_string, idx)
            has_leading_zero = bool(re.search(r"\b0\d+\b", match[0]))
            if has_leading_zero:
                raise ValueError("Invalid number with leading zero.")
            num = float(match[0])
            num = int(num) if num.is_integer() else num
            tokens.append(JSONToken(TokenType.NUMBER, num))
            end_idx = match.end()
            idx = end_idx - 1
        idx += 1
    return tokens


def parse_tokens_fsm(tokens: List[JSONToken]):
    state = ParserState.START_OBJECT
    idx = 0
    stack = []
    current_object = {}  # this can be an array or a dict depending on the context
    current_key = None
    while idx < len(tokens):
        token = tokens[idx]
        # if state == ParserState.START_PARSING:
        #     if token.token_type == TokenType.LEFT_BRACE:
        #         state = ParserState.START_OBJECT
        #     elif token.token_type == TokenType.LEFT_BRACKET:
        #         current_object = []
        #         state = ParserState.READ_VALUE
        #     elif (
        #         token.token_type
        #         in {
        #             TokenType.STRING,
        #             TokenType.NUMBER,
        #             TokenType.BOOLEAN,
        #             TokenType.NULL,
        #         }
        #         and idx == len(tokens) - 1
        #     ):
        #         return token.value
        #     else:
        #         raise ValueError("Unexpected token at the start of input.")

        if state == ParserState.START_OBJECT:
            if token.token_type == TokenType.LEFT_BRACE:
                state = ParserState.READ_KEY
            else:
                raise ValueError("Expected '{' to start an object.")

        elif state == ParserState.READ_KEY:
            if token.token_type == TokenType.STRING:
                current_key = token.value
                state = ParserState.READ_COLON
            elif token.token_type == TokenType.RIGHT_BRACE:
                nested_obj = current_object
                if len(stack) > 0:
                    current_object, current_key = stack.pop()
                    current_object[current_key] = nested_obj
                state = ParserState.END_OBJECT
            elif idx == len(tokens) - 1:
                raise ValueError("Unexpected end of input.")
            else:
                raise ValueError("Expected a string as key.")

        elif state == ParserState.READ_COLON:
            if token.token_type == TokenType.COLON:
                state = ParserState.READ_VALUE
            else:
                raise ValueError("Expected ':' after key.")

        elif state == ParserState.READ_VALUE:
            if token.token_type in {
                TokenType.STRING,
                TokenType.NUMBER,
                TokenType.BOOLEAN,
                TokenType.NULL,
            }:
                if isinstance(current_object, dict):
                    current_object[current_key] = token.value
                else:  # array
                    current_object.append(token.value)
                state = ParserState.READ_COMMA
            elif token.token_type == TokenType.LEFT_BRACE:
                stack.append((current_object, current_key))
                current_object = {}
                state = ParserState.READ_KEY
            elif token.token_type == TokenType.LEFT_BRACKET:
                stack.append((current_object, current_key))
                current_object = []
                state = ParserState.READ_VALUE
            elif token.token_type == TokenType.RIGHT_BRACKET and isinstance(
                current_object, list
            ):
                nested_array = current_object
                if len(stack) > 0:
                    current_object, current_key = stack.pop()
                    current_object[current_key] = nested_array
                state = ParserState.READ_COMMA
            else:
                raise ValueError("Unexpected token while reading value.")

        elif state == ParserState.READ_COMMA:
            if token.token_type == TokenType.COMMA:
                if idx + 1 < len(tokens):
                    next_token = tokens[idx + 1]
                    if next_token.token_type in {
                        TokenType.RIGHT_BRACE,
                        TokenType.RIGHT_BRACKET,
                    }:
                        raise ValueError("Unexpected trailing comma")
                elif idx == len(tokens) - 1:
                    raise ValueError("Unexpected end of input.")
                state = (
                    ParserState.READ_KEY
                    if isinstance(current_object, dict)
                    else ParserState.READ_VALUE
                )
            elif token.token_type == TokenType.RIGHT_BRACE and isinstance(
                current_object, dict
            ):
                nested_obj = current_object
                if len(stack) > 0:
                    current_object, current_key = stack.pop()
                    current_object[current_key] = nested_obj
                state = ParserState.END_OBJECT
            elif token.token_type == TokenType.RIGHT_BRACKET and isinstance(
                current_object, list
            ):
                nested_array = current_object
                if len(stack) > 0:
                    current_object, current_key = stack.pop()
                    current_object[current_key] = nested_array
                state = ParserState.READ_COMMA
            else:
                raise ValueError("Unexpected token. Expected ',' or closing bracket.")

        elif state == ParserState.END_OBJECT:
            if token.token_type == TokenType.RIGHT_BRACE:
                nested_obj = current_object
                if len(stack) > 0:
                    current_object, current_key = stack.pop()
                    current_object[current_key] = nested_obj

        idx += 1
    if len(stack) > 0:
        raise ValueError("Unclosed bracket(s).")
    return current_object


def parse_object(tokens: List[JSONToken]):
    obj = {}
    key = None
    value_token_types = [
        TokenType.STRING,
        TokenType.BOOLEAN,
        TokenType.NUMBER,
        TokenType.NULL,
        TokenType.LEFT_BRACE,  # arrays
        TokenType.LEFT_BRACKET,  # objects
    ]
    valid_next_tokens = value_token_types + [TokenType.RIGHT_BRACE]
    idx = 0
    while idx < len(tokens):
        token = tokens[idx]
        debug_print("Processing: " + str(token.value))
        if token.token_type not in valid_next_tokens:
            raise ValueError(f"Invalid token: {token}")
        if token.token_type == TokenType.RIGHT_BRACE:
            return obj, idx
        elif token.token_type == TokenType.LEFT_BRACE:
            nested_obj, end_idx = parse_object(tokens[idx + 1 :])
            obj[key] = nested_obj
            key = None
            valid_next_tokens = [TokenType.COMMA, TokenType.RIGHT_BRACE]
            idx = end_idx
        elif token.token_type == TokenType.LEFT_BRACKET:
            nested_array, end_idx = parse_array(tokens[idx + 1 :])
            obj[key] = nested_array
            key = None
            valid_next_tokens = [TokenType.COMMA, TokenType.RIGHT_BRACE]
            idx = end_idx
        elif token.token_type == TokenType.STRING:
            if key is None:  # string is the key
                key = token.value
                valid_next_tokens = [TokenType.COLON]
            else:  # string is the value for the existing key
                obj[key] = token.value
                key = None
                valid_next_tokens = [TokenType.COMMA, TokenType.RIGHT_BRACE]
        elif token.token_type == TokenType.COLON:
            valid_next_tokens = value_token_types  # any value can come after a colon
        elif token.token_type == TokenType.COMMA:
            key = None
            valid_next_tokens = [TokenType.STRING]  # keys must be strings
        elif key is not None and token.token_type in [
            TokenType.BOOLEAN,
            TokenType.NUMBER,
            TokenType.NULL,
        ]:
            obj[key] = token.value
            key = None
            valid_next_tokens = [TokenType.COMMA, TokenType.RIGHT_BRACE]
        idx += 1
    return obj, idx


def parse_array(tokens: List[JSONToken]):
    array = []
    value_token_types = [
        TokenType.STRING,
        TokenType.BOOLEAN,
        TokenType.NUMBER,
        TokenType.NULL,
    ]
    valid_next_tokens = value_token_types
    idx = 0
    while idx < len(tokens):
        token = tokens[idx]
        if token.token_type not in valid_next_tokens:
            raise ValueError(f"Invalid token: {token}")
        if token.token_type == TokenType.RIGHT_BRACKET:
            return array, idx
        elif token.token_type in value_token_types:
            array.append(token.value)
            valid_next_tokens = [TokenType.COMMA, TokenType.RIGHT_BRACKET]
        elif token.token_type == TokenType.COMMA:
            valid_next_tokens = value_token_types  # any value can come after a comma
        idx += 1
    return array, idx


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
