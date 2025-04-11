# CUDX Encryption Tool 🛡️

A unique command-line encryption tool that combines phone keypad mapping with a dynamic Up/Down shifting pattern and a visual disambiguation schema.

## What is CUDX? 🤔

CUDX is a custom substitution cipher method with several layers:

1.  **Phone Keypad Mapping:** Converts letters to their corresponding numbers on a standard phone keypad (e.g., A, B, C -> 2; D, E, F -> 3).
2.  **CUD Pattern (Cipher Up/Down):** Applies a user-defined pattern of 'U' (Up) and 'D' (Down) shifts to the numeric code, making simple frequency analysis difficult.
3.  **Scope Control:** Allows the user to define how the CUD pattern resets: per word, per sentence, or per paragraph.
4.  **Disambiguation Schema:** Generates a unique visual schema using dots (`.`) and asterisks (`*`) to pinpoint the original letter on its corresponding keypad number, solving the ambiguity where multiple letters map to the same number.

## Features ✨

* Encrypts English text messages.
* Uses a customizable Up/Down shifting pattern (`CUD...`).
* Provides flexible pattern application scope (Word `1`, Sentence `11`, Paragraph `111`).
* Generates a clear, column-based visual schema for decryption ambiguity.
* Includes basic input validation and user guidance.
* Command-line interface for easy use.

## How it Works ⚙️

1.  **Input:** The script prompts the user for the text to encrypt, the CUD pattern (e.g., `UD`, `UUDD`), and the scope (1, 11, or 111).
2.  **Initial Conversion:** The input text (uppercase English letters, space ` `, period `.`, slash `/`) is converted into a sequence of numbers and symbols based on the phone keypad map.
3.  **CUD Pattern Application:** The chosen CUD pattern (e.g., `C`+`UD` -> `CUD`) is extended to match the length of the message. It's then applied sequentially based on the selected scope:
    * `U`: Increments the number.
    * `D`: Decrements the number.
    * The pattern index (`cud_index`) resets based on the scope rules (word, sentence, or paragraph breaks).
4.  **Schema Generation:** For each character in the *original* valid input, a dot-pattern is generated indicating its position on the phone key (e.g., for key `2 = ABC`, `A` is `*..`, `B` is `.*.`, `C` is `..*`). Special characters also get unique patterns (`++++` for space, `----` for period, `////` for slash).
5.  **Output:** The script prints:
    * The final CUDX-encrypted numeric sequence.
    * The visual disambiguation schema, arranged in columns.
    * The CUDX pattern and scope used.

## Usage Example 🚀

1.  Save the code as a Python file (e.g., `cudx_encrypt.py`).
2.  Run it from your terminal: `python cudx_encrypt.py`
3.  Follow the prompts:

```bash
Welcome to the CUDX Encryption Program.

Would you like information about CUDX? [Y]es <> [N]o :N
Looks like you already know!
What do you want to encrypt? ----> (Use English characters, put '.' at the end of sentences, put '/' at the end of paragraphs, DO NOT USE NUMBERS.)HELLO. WORLD/
Initial numeric code (valid chars only): [4, 3, 5, 5, 6, '-', '+', 9, 6, 7, 5, 3, '/']

How do you want the CUDX repetition pattern to be? (e.g., CUUD) ---> CUD
In texts written with the CUDX Encryption method, the application method of the CUDX pattern will create differences in the cipher.

    Application Scope of the CUDX Pattern;

    For word-based application (resets index at '+' space): 1
    For sentence-based application (resets index at '-' period): 11
    For paragraph-based application (resets index at '/' slash): 111

Enter scope (1, 11, or 111): 11

----------- Your CUDX cipher schema -----------
. . . . . - + * . * . . /
* * * * * - + . * . * * /
. . . . . - + . . . . . /
. . . . . - + . . . . . /

Your Cipher : [5, 2, 6, 4, 7, '-', '+', 10, 5, 8, 4, 4, '/']
Your CUDX Pattern : CUD11
