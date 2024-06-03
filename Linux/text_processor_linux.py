import file_handler_linux as fh


def clean_filename(filename: str):
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

def linebreak_file(file_path: str):
    ''' Takes in filepath. Reads file in filepath. Returns list of lines in file.
    '''
    cleaned_file = []

    file = open(r"{}".format(file_path), 'r', encoding='utf8')
    split_file = file.read().split("\n")

    for line in split_file:
        cleaned_file.append(line.replace("\xa0", " "))

    return cleaned_file

def test_line(cleaned_file: list, line_num: int):
    ''' Takes in file as list and line number. Check file line and following for type and returns
        True for type.
    '''
    timecode = False
    slide = False
    line_break = False
    text = False
    timecode_key = "-->"

    try:
        line = cleaned_file[line_num]
    except IndexError:
        return False, False, False, False

    try:
        if int(line):
            slide = True
    except ValueError:
        pass

    if slide is False:
        if timecode_key in line:
            timecode = True
        elif line == "\n" or line == "":
            line_break = True
        else:
            text = True

    return slide, timecode, line_break, text

def fix_chars(word: str):
    ''' Takes in word. Replaces characters incompatible with Latin-1.
    '''
    problem_chars = {
        "♪": "", # existing character: replacement value
        "’": "'",
        "“": "\"",
        "”": "\"",
        "…": "..."}

    for key in problem_chars:
        if key in word:
            word = word.replace(key, problem_chars[key])

    return word

# split lines into 32 char or less each
def split_lines(line: str):
    ''' Takes in line as string. If line > 32char, splits into multiple lines.
        Returns list of newlines.
    '''
    length = 0
    count = 0
    newlines = [[],[], [], []]

    split_line = line.strip().split(" ")

    for word in split_line:
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

def process_file(cleaned_file: list):
    ''' Takes in list of file lines. Calls functions to format lines. Returns list of lines.
    '''
    timecode, line_break = False, False
    next_text = False
    line1, line2, combined = "", "", ""
    count = 0
    skip_next = False
    rev_lines = [[], [], [], []]
    printline = ""
    to_write = []

    for line in cleaned_file:
        if skip_next:
            skip_next = False
            count += 1

        else:
            slide, timecode, line_break, _ = test_line(cleaned_file, count)

            if slide:
                to_write.append(line)
            elif timecode:
                to_write.append(line)
            elif line_break:
                pass
            else:
                _, _, _, next_text = test_line(cleaned_file, count + 1)
                if next_text:
                    line1 = line.strip().split(" ")
                    line2 = cleaned_file[count + 1].strip().split(" ")
                    combined = line1 + line2
                    combined = " ".join(combined)
                else:
                    combined = line

                rev_lines = split_lines(combined)

                for revline in rev_lines:
                    if len(revline) != 0:
                        printline = " ".join(revline)
                        to_write.append(printline)

                to_write.append("\n")

                skip_next = True

            count += 1
            slide, timecode, line_break, _ = False, False, False, False
            _, _, _, next_text = False, False, False, False

    return to_write

def main(path: str, file: str):
    ''' Takes in filepath and file as strings. Calls functions to process files and write
        reformatted data to file.
    '''
    new_filename = clean_filename(file)
    file_path = path + file
    cleaned_file = linebreak_file(file_path)
    new_file = process_file(cleaned_file)
    fh.write_file(path, new_file, new_filename)


if __name__ == '__main__':
    main()