'''
    This module takes a filepath and filename as strings. It processes the
    lines of text within the file such that each text line (not including
    numeric indicators and time codes) is no more than 32 characters long.
    It then saves the newly formatted text to a file in the same location as
    the original file with the tag '-Formatted' appended to the filename.
'''

def clean_filename(filename):
    ''' Takes in filename string. Returns filename cleaned of ()s and spaces
        and tagged with '-Formatted' at the end.
    '''
    format_declaration = "unformatted"

    split = filename.split('.')
    fname = split[0]

    if format_declaration in fname.lower():
        fname = fname.replace(format_declaration, "Formatted")
    else:
        fname = "{}{}".format(fname, "-Formatted")

    extension = '.' + split[1]
    cleaned = fname.replace(' ', '-').replace('(', '').replace(')', '')
    new_file = cleaned + extension

    return new_file

def linebreak_file(file_path):
    ''' Takes in filepath. Reads file in filepath. Returns list of lines in file.
    '''
    cleaned_file = []

    with open(file_path, 'r', encoding='utf8') as f:
        split_file = f.read().split("\n")
    f.close()

    for line in split_file:
        cleaned_file.append(line.replace("\xa0", " "))

    return cleaned_file

def test_line(cleaned_file, line_num):
    ''' Takes in file as list and line number. Check file line and following for type and returns
        True for type.
    '''
    timecode = False
    slide = False
    line_break = False
    text = []
    timecode_key = "-->"

    try:
        line = cleaned_file[line_num]
    except IndexError:
        return False, False, False, [False]

    for x in range(10):
        try:
#            print(f"test_line try slide: {cleaned_file[line_num + x]}")
            if int(cleaned_file[line_num + x]) and not text:
                slide = True
                break
            else:
                break
        except ValueError:
            pass

        if slide is False:
            if timecode_key in cleaned_file[line_num + x] and not text:
                timecode = True
                break
            elif timecode_key in cleaned_file[line_num + x]:
                break
            elif cleaned_file[line_num + x] == "\n" or cleaned_file[line_num + x] == "" \
                and not text:
                line_break = True
                break
            elif cleaned_file[line_num + x] == "\n" or cleaned_file[line_num + x] == "":
                break
            else:
                text.append(True)
                print(f"testline text: {text}")

    return slide, timecode, line_break, text

def fix_chars(word):
    ''' Takes in word. Replaces characters incompatible with Latin-1.
    '''
    problem_chars = {
        "♪": "", # base character, replacement value
        "’": "'",
        "“": "\"",
        "”": "\"",
        "…": "..."}

    for key in problem_chars:
        if key in word:
            word = word.replace(key, problem_chars[key])

    return word

def split_lines(line):
    ''' Takes in line as string. If line > 32char, splits into multiple lines.
        Returns list of newlines.
    '''
    length = 0
    count = 0
    newlines = [[],[], [], [], []]

#    print(f"line: {line}")
    split_line = line.strip().split(" ")
#    print(f"split line: {split_line}")

    for word in split_line:
#        print(word)
        clean_word = fix_chars(word)
        if len(clean_word) == 0:
            continue
        else:
            if (length + len(clean_word) + 1) <= 32:
                length += len(clean_word) + 1
                newlines[count].append(clean_word)
            else:
                count += 1
                length = 0
                newlines[count].append(clean_word)
                length += len(clean_word) + 1

    return newlines

def process_file(cleaned_file):
    ''' Takes in list of file lines. Calls functions to format lines. Returns list of lines.
    '''
    timecode, line_break = False, False
    line1, combined = "", ""
    skip_next = [False]
    rev_lines = [[], [], [], []]
    printline = ""
    to_write = []

    for i, line in enumerate(cleaned_file):
        print(f"Line: {i, line}")
        if skip_next:
            del skip_next[0]

        else:
            slide, timecode, line_break, text_test = test_line(cleaned_file, i)
            print(f"{slide}, {timecode}, {line_break}, {text_test}")
            if slide:
                print(f"{i}, slide")
                to_write.append(line)
            elif timecode:
                print(f"{i}, timecode")
                to_write.append(line)
            elif line_break:
                print("linebreak")
                pass
            else:
                _, _, _, next_text = test_line(cleaned_file, i)
                print(f"process_file else: {i}, {line}")
                if next_text[0]:
                    combined = []
                    for x, y in enumerate(next_text):
                        line1 = cleaned_file[i + x].strip().split(" ")
                        combined = combined + line1
                    print(combined)
                    combined = " ".join(combined)

                    skip_next = next_text

#                else:
#                    combined = line

                rev_lines = split_lines(combined)

                for revline in rev_lines:
                    if len(revline) != 0:
                        printline = " ".join(revline)
                        to_write.append(printline)

                to_write.append("\n")

            slide, timecode, line_break, _ = False, False, False, False
            _, _, _, next_text = False, False, False, False

    return to_write

def write_file(dir_path: str, text: list, new_filename: str):
    ''' Takes directory path and filename as strings and file text as a list. Writes and saves
        text to file in directory path.
    '''
    with open(dir_path + new_filename, 'w', encoding='latin1') as f:

        for line in text:
            f.write(line)
            f.write("\n")

    f.close()

def main(path, file):
    ''' Takes in filepath and file as strings. Calls functions to process files and write
        reformatted data to file.
    '''
    new_filename = clean_filename(file)
    file_path = path + file
    cleaned_file = linebreak_file(file_path)
    new_file = process_file(cleaned_file)
    write_file(path, new_file, new_filename)


if __name__ == '__main__':
    main()
