from itertools import zip_longest, chain
import sys # Needed for exiting early if input is invalid

# CUDX.py
def cudx():
    # Phone keypad mapping: Letter -> Number, Space -> '+', Period -> '-', Slash -> '/'
    telefon_klavyesi = {"A": 2, "B": 2, "C": 2, "D": 3, "E": 3, "F": 3,
                        "G": 4, "H": 4, "I": 4, "J": 5, "K": 5, "L": 5, "M": 6,
                        "N": 6, "O": 6,
                        "P": 7, "Q": 7, "R": 7, "S": 7, "T": 8,
                        "U": 8, "V": 8, "W": 9, "X": 9, "Y": 9, "Z": 9, " ": "+", ".": "-", "/": "/"}
    # Lists of letters for each number key (used for schema generation)
    tel_k2 = ["A", "B", "C"]
    tel_k3 = ["D", "E", "F"]
    tel_k4 = ["G", "H", "I"]
    tel_k5 = ["J", "K", "L"]
    tel_k6 = ["M", "N", "O"]
    tel_k7 = ["P", "Q", "R", "S"]
    tel_k8 = ["T", "U", "V"]
    tel_k9 = ["W", "X", "Y", "Z"]
    # Full alphabet list (including Q, W, X - might be slightly redundant but used for checks)
    alfabe = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "R", "S", "T", "U", "V",
                "Y", "Z", "Q", "W", "X"]


    metin_sifre1 = list()  # initially generated code (numeric representation)
    metin_sifre2 = list()  # CUDX'ed code (after applying U/D shifts)
    valid_metin_chars = [] # Store chars that are actually processed
    skipped_chars = set()  # Store chars that were skipped

    # Get input text from the user
    metin = (input(
        "What do you want to encrypt? ----> (Use English characters, put '.' at the end of sentences, put '/' at the end of paragraphs, DO NOT USE NUMBERS.)"))

    # --- Input Character Validation (Fix for E1: KeyError) ---
    # Convert input text to initial numeric code, handling undefined characters
    for harf in metin.upper():
        numeric_val = telefon_klavyesi.get(harf) # Use .get() to avoid KeyError
        if numeric_val is not None:
            metin_sifre1.append(numeric_val)
            valid_metin_chars.append(harf) # Store the valid original char for schema
        else:
            skipped_chars.add(harf) # Track skipped characters

    # Warn if characters were skipped
    if skipped_chars:
        # Sort skipped characters for consistent output
        skipped_list = sorted(list(skipped_chars))
        print(f"\nWarning: The following characters were skipped as they are not defined in the keypad mapping: {', '.join(skipped_list)}")

    # Check if any valid characters remain to be processed
    if not metin_sifre1:
         print("Error: No valid characters found in the input text to encrypt. Exiting.")
         return # Exit the function if nothing to process

    print("\nInitial numeric code (valid chars only):", metin_sifre1)

    # Get the CUD (Up/Down) pattern from the user
    cud_duzeni = input("How do you want the CUDX repetition pattern to be? (e.g., CUUD) ---> C")
    # cudx = pattern received for cipher 2
    sayac = 0 # counter for extending the pattern
    ilkcud = cud_duzeni # store the original short pattern
    # No need to convert cud_duzeni to list, string indexing works fine

    # CUD pattern extension section: Make the pattern at least as long as the *valid* message length
    while len(metin_sifre1) > len(cud_duzeni):
        # Prevent IndexError if original pattern is empty
        if not ilkcud:
            print("Error: CUD pattern cannot be empty if message is not empty. Exiting.")
            return
        # Cycle through the original pattern using modulo
        cud_duzeni = cud_duzeni + ilkcud[sayac % len(ilkcud)]
        sayac += 1

    # Explain the pattern application scope options
    print(''' \nIn texts written with the CUDX Encryption method, the application method of the CUDX pattern will create differences in the cipher.

    Application Scope of the CUDX Pattern;

    For word-based application (resets index at '+' space): 1
    For sentence-based application (resets index at '-' period): 11
    For paragraph-based application (resets index at '/' slash): 111
    ''')

    # --- Scope Input Validation (Fix for E2: ValueError & I3: Unhandled Scope) ---
    while True: # Loop until valid input is received
        try:
            wsp_input = input("Enter scope (1, 11, or 111): ")
            wsp = int(wsp_input)
            if wsp in [1, 11, 111]:
                break # Valid input, exit loop
            else:
                # Handle integer values other than 1, 11, 111
                print("Error: Invalid scope value. Please enter exactly 1, 11, or 111.")
        except ValueError:
            # Handle non-integer input
            print("Error: Invalid input. Please enter a number (1, 11, or 111).")

    cud_index = 0 # Index for the current position in the CUD pattern
    # Apply the CUD pattern based on the chosen scope (wsp)
    # Iterating through metin_sifre1 which only contains valid numeric/separator codes
    if wsp == 1: # Word-based
        for sayi in metin_sifre1:
            if isinstance(sayi, int): # Check if it's a number (safer than checking != "+", etc.)
                if cud_index < len(cud_duzeni): # Ensure index is within bounds
                     if cud_duzeni[cud_index].upper() == "U":
                         metin_sifre2.append(sayi + 1)
                         cud_index += 1
                     elif cud_duzeni[cud_index].upper() == "D":
                         metin_sifre2.append(sayi - 1)
                         cud_index += 1
                     else: # Handle case where pattern contains non U/D chars (optional)
                         metin_sifre2.append(sayi) # Append unchanged number
                         cud_index += 1 # Still advance pattern index
                else: # Should not happen due to pattern extension, but as safeguard
                    metin_sifre2.append(sayi)
            elif sayi == "+": # Space
                metin_sifre2.append("+")
                cud_index = 0 # Reset pattern index for new word
            elif sayi == "-": # Period
                metin_sifre2.append("-")
                cud_index = 0 # Reset pattern index (word-based scope)
            elif sayi == "/": # Slash
                metin_sifre2.append("/")
                cud_index = 0 # Reset pattern index (word-based scope)
    elif wsp == 11: # Sentence-based
        for sayi in metin_sifre1:
             if isinstance(sayi, int):
                 if cud_index < len(cud_duzeni):
                     if cud_duzeni[cud_index].upper() == "U":
                         metin_sifre2.append(sayi + 1)
                         cud_index += 1
                     elif cud_duzeni[cud_index].upper() == "D":
                         metin_sifre2.append(sayi - 1)
                         cud_index += 1
                     else:
                         metin_sifre2.append(sayi)
                         cud_index += 1
                 else:
                    metin_sifre2.append(sayi)
             elif sayi == "+": # Space
                 metin_sifre2.append("+")
                 cud_index += 1 # Pattern continues across spaces within a sentence
             elif sayi == "-": # Period
                 metin_sifre2.append("-")
                 cud_index = 0 # Reset pattern index for new sentence
             elif sayi == "/": # Slash
                 metin_sifre2.append("/")
                 cud_index = 0 # Reset pattern index (sentence-based scope includes paragraph reset)
    elif wsp == 111: # Paragraph-based
        for sayi in metin_sifre1:
            if isinstance(sayi, int):
                 if cud_index < len(cud_duzeni):
                     if cud_duzeni[cud_index].upper() == "U":
                         metin_sifre2.append(sayi + 1)
                         cud_index += 1
                     elif cud_duzeni[cud_index].upper() == "D":
                         metin_sifre2.append(sayi - 1)
                         cud_index += 1
                     else:
                        metin_sifre2.append(sayi)
                        cud_index += 1
                 else:
                    metin_sifre2.append(sayi)
            elif sayi == "+": # Space
                metin_sifre2.append("+")
                cud_index += 1 # Pattern continues across spaces
            elif sayi == "-": # Period
                metin_sifre2.append("-")
                # --- Keeping original logic as requested (Potential Error 3 NOT fixed) ---
                cud_index = 1 # Pattern index set to 1 after period in paragraph mode
                # --- End of potentially incorrect logic ---
            elif sayi == "/": # Slash
                metin_sifre2.append("/")
                cud_index = 0 # Reset pattern index for new paragraph

    # --- Schema Generation ---
    kod_listesi = [] # List to hold the dot-pattern strings for each character
    # Generate the dot pattern only for the characters that were successfully processed
    for thing in valid_metin_chars: # Use the list of valid original characters
        if thing in alfabe: # If it's a letter
            # Check keys with 3 letters (2, 3, 4, 5, 6, 8)
            if thing in tel_k2 or thing in tel_k3 or thing in tel_k4 or thing in tel_k5 or thing in tel_k6 or thing in tel_k8:
                if thing == tel_k2[0] or thing == tel_k3[0] or thing == tel_k4[0] or thing == tel_k5[0] or thing == tel_k6[0] or thing == tel_k8[0]:
                    kod_listesi.append("*.. £") # First letter pattern
                elif thing == tel_k2[1] or thing == tel_k3[1] or thing == tel_k4[1] or thing == tel_k5[1] or thing == tel_k6[1] or thing == tel_k8[1]:
                    kod_listesi.append(".*. £") # Second letter pattern
                elif thing == tel_k2[2] or thing == tel_k3[2] or thing == tel_k4[2] or thing == tel_k5[2] or thing == tel_k6[2] or thing == tel_k8[2]:
                    kod_listesi.append("..* £") # Third letter pattern
            # Check keys with 4 letters (7, 9)
            elif thing in tel_k7 or thing in tel_k9:
                if thing == tel_k7[0] or thing == tel_k9[0]:
                    kod_listesi.append("*...£") # First letter pattern
                elif thing == tel_k7[1] or thing == tel_k9[1]:
                    kod_listesi.append(".*..£") # Second letter pattern
                elif thing == tel_k7[2] or thing == tel_k9[2]:
                    kod_listesi.append("..*.£") # Third letter pattern
                elif thing == tel_k7[3] or thing == tel_k9[3]:
                    kod_listesi.append("...*£") # Fourth letter pattern
        elif thing == " ": # Space
            kod_listesi.append("++++£") # Space pattern
        elif thing == ".": # Period
            kod_listesi.append("----£") # Period pattern
        elif thing == "/": # Slash
            kod_listesi.append("////£") # Slash pattern
        # No else needed because valid_metin_chars only contains processable chars

    # Flatten the list of dot-pattern strings into a single list of characters ('*', '.', '£', '+', '-')
    result = list(chain.from_iterable(list(txt) for txt in kod_listesi))
    # print(result) # Optional: print the flattened list

    print("\n----------- Your CUDX cipher schema -----------")

    # Function to arrange the flattened schema characters into columns based on the '£' delimiter
    def construct_columns(result):
        columns = [[]]
        current_column_number = 0
        for item in result:
            if item == "£": # Delimiter marks the end of a character's pattern
                columns.append([])
                current_column_number += 1
            else:
                # Ensure index is valid before appending
                if current_column_number < len(columns):
                     columns[current_column_number].append(item)
        # Remove the last empty list if it exists (due to trailing '£')
        if columns and not columns[-1]:
             columns.pop()
        return columns

    # Main function to print the schema in a grid format
    def main():
        columns = construct_columns(result)
        # Transpose columns into rows for printing, filling short columns with spaces
        # Check if columns is not empty before proceeding
        if columns:
             rows = list(zip_longest(*columns, fillvalue=' '))
             for row in rows:
                 print(" ".join(row)) # Print each row with spaces between characters
        else:
            print("(Schema is empty)") # Handle case where schema might be empty

    
    main() # Call the main function to print the schema

    # Print the final CUDX-encrypted numeric code
    print("\nYour Cipher : {}".format(metin_sifre2))
    # Print the CUDX pattern used, including the scope indicator (1, 11, or 111)
    print("Your CUDX Pattern : C" + ilkcud.upper() + str(wsp))

# --- Program Start ---
print("\nWelcome to the CUDX Encryption Program.")
# Ask if the user wants information about the CUDX method
# Using a loop for Yes/No input validation
while True:
    bilgi = input("Would you like information about CUDX? [Y]es <> [N]o :").strip().upper()
    if bilgi in ["Y", "N"]:
        break
    else:
        print("Invalid input. Please enter 'Y' for Yes or 'N' for No.")

if bilgi == "Y":
    # Print the explanation of the CUDX method
    print('''~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
CUDX Encryption Method -by Faruk Yiğit Oluşan

CUDX writes words based on the letters under the phone numbers.
I.e., 2 ABC, 3 DEF, ...., 9 WXYZ . USE ENGLISH CHARACTERS WHEN WRITING, DO NOT USE NUMBERS. Place SPACE after .'s and /'s.

e.g., AHMET = 24638

Then, an increment-decrement pattern is determined with U and D letters (up / down).
U and D can be added in the desired pattern after the letter C.

e.g., If our code is CUD, we increase and decrease the numbers by 1 in sequence.

UDUDU
24638 --> 33729   Thus, the text cannot be guessed by looking at letter repetitions.

As in the example above, our UD rule consisting of 2 letters could not be completed because the word has 5 letters.
Now we have another problem. Will the next word continue with D, or will the code restart from the beginning for each word?

We solve this problem by adding a 1 (or 11 or 111) to the end of the CUD code we wrote.

If we add one "1", the rule starts over for each word (word-based).
If we add two "1"s ("11"), the rule continues for each sentence (sentence-based, resets at '.').
If we add three "1"s ("111"), it continues until the end of the paragraph/text (paragraph-based, resets at '/').

Now: We have the code 33729 and CUD1 (if word-based was chosen) showing how it was incremented, but there is one last problem.

Even if the person receiving the message applies the rule in reverse and reaches our initial cipher 24638,
they have at least 3 (like A,B,C for 2), and sometimes 4 (like P,Q,R,S for 7), options for each number.
To prevent this ambiguity, we need the CUDX Cipher Schema.

(A) G (M) D (T)          * . * . *
 B (H) N (E) U    --->   . * . * .    With these dots (schema), we secretly tell the
 C  I  O  F  V           . . . . .    receiver exactly which letters they are.

THE END ...
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~''')
    # Ask if the user is ready to proceed after reading the info
    # Using a loop for Yes/No input validation
    while True:
        baslangic = input("Are you ready to encrypt your message? [Y]es / [N]o: ").strip().upper()
        if baslangic in ["Y", "N"]:
            break
        else:
            print("Invalid input. Please enter 'Y' for Yes or 'N' for No.")

    if baslangic == "Y":
        cudx() # Start the encryption process
    else:
        print("See you later...")
        sys.exit() # Exit if user chooses not to proceed
else:
    # If the user didn't want info, proceed directly to encryption
    print("Looks like you already know!")
    cudx() # Start the encryption process