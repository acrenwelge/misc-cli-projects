# JSON Parser Finite State Machine (FSM) Instructions

## General Setup

1. Start with the `START_OBJECT` state for the entire JSON document.
2. Use a stack to keep track of parent structures (objects or arrays) during nested parsing.
3. Maintain a `current_object` to hold the structure being built (dictionary for objects or list for arrays).
4. Maintain a `current_key` to store the key when parsing objects.

## States for Objects

### START_OBJECT

1. Expect a `{` token to begin the object. Push the current context onto the stack and initialize a new dictionary as `current_object`.
2. Transition to `READ_KEY`.

### READ_KEY

1. Expect a `STRING` token representing a key, or a `}` token to close the object:
    - If `STRING`: Store the key in `current_key` and transition to `READ_COLON`.
    - If `}`: Pop the stack to return to the parent structure. If the stack is empty, parsing is complete; otherwise, transition back based on the parent type (`READ_COMMA` for objects, `READ_VALUE` for arrays).
    - Otherwise, raise an error.

### READ_COLON

1. Expect a `:` token after the key. Transition to `READ_VALUE`.

### READ_VALUE

1. Expect one of the following tokens:
    - `STRING`, `NUMBER`, `BOOLEAN`, or `NULL`: Add the key-value pair to `current_object`. Transition to `READ_COMMA`.
    - `{`: Push the current context onto the stack. Initialize a new dictionary as `current_object` and transition to `READ_KEY`.
    - `[`: Push the current context onto the stack. Initialize a new list as `current_object` and transition to `READ_VALUE`.
    - Otherwise, raise an error.

### READ_COMMA

1. Expect a `,` token to indicate another key-value pair, or a `}` token to close the object:
    - If `,`: Transition to `READ_KEY`.
    - If `}`: Pop the stack to return to the parent structure. Transition back based on the parent type (`READ_COMMA` for objects, `READ_VALUE` for arrays).
    - Otherwise, raise an error.

## States for Arrays

### START_ARRAY

1. Expect a `[` token to begin the array. Push the current context onto the stack and initialize a new list as `current_array`.
2. Transition to `READ_VALUE`.

### READ_VALUE

1. Expect one of the following tokens:
    - `STRING`, `NUMBER`, `BOOLEAN`, or `NULL`: Add the value to `current_array`. Transition to `READ_COMMA`.
    - `{`: Push the current context onto the stack. Initialize a new dictionary as `current_object` and transition to `READ_KEY`.
    - `[`: Push the current context onto the stack. Initialize a new list as `current_array` and transition to `READ_VALUE`.
    - `]`: Pop the stack to return to the parent structure. Transition back based on the parent type (`READ_COMMA` for objects, `READ_VALUE` for arrays).
    - Otherwise, raise an error.

### READ_COMMA

1. Expect a `,` token to indicate another value, or a `]` token to close the array:
    - If `,`: Transition to `READ_VALUE`.
    - If `]`: Pop the stack to return to the parent structure. Transition back based on the parent type (`READ_COMMA` for objects, `READ_VALUE` for arrays).
    - Otherwise, raise an error.

## Final State

1. When the stack is empty and no tokens are left to process, the parsing is complete.
2. If tokens remain but the stack is empty, or an invalid token is encountered, raise an error.

## Key Principles

1. **Maintain Context**: Always push the current context (parent object or array) onto the stack when transitioning to a nested structure.
2. **Validate Tokens**: Ensure that every token matches the expected type for the current state.
3. **Pop Context**: When closing an object or array (`}` or `]`), pop the stack and restore the parent context.
4. **Handle Edge Cases**: Account for empty objects (`{}`) and arrays (`[]`) by transitioning correctly from `START_OBJECT` or `START_ARRAY` to their respective ending states.