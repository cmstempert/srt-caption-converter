import file_handler_macos as fh

# clean up file name
def clean_filename(filename):
    format_declaration = "unformatted"

    split = filename.split('.')
    fname = split[0]
    
    if format_declaration in fname.lower():
        fname = fname.replace(format_declaration, "Formatted")
    else:
        fname = ("{}{}".format(fname, "-Formatted"))

    extension = '.' + split[1]
    cleaned = fname.replace(' ', '-').replace('(', '').replace(')', '')
    new_file = cleaned + extension

    return new_file

# break file into lines and clean up weird space characters
def linebreak_file(file_path):
    cleaned_file = []
    
    file = open(file_path, 'r')
    split_file = file.read().split("\n")

    for line in split_file:
        cleaned_file.append(line.replace("\xa0", " "))
    
    return cleaned_file

# tests lines for type (slide, timecode, blank, text)
def test_line(cleaned_file, line_num):
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

# replace non-latin characters
def fix_chars(word):
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

# split lines into 32 char or less each
def split_lines(line):
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

# processes raw file, return list to write to new file
def process_file(cleaned_file):
    timecode, clide, line_break, text = False, False, False, False
    next_slide, next_timecode, next_linebreak, next_text = False, False, False, False
    line1, line2, combined = "", "", ""
    count = 0
    skip_next = False
    rev_lines = [[], [], [], []]
    rline_count = 0
    printline = ""
    to_write = []

    for line in cleaned_file:
        if skip_next:
            skip_next = False
            count += 1

        else:
            slide, timecode, line_break, text = test_line(cleaned_file, count)

            if slide:
                to_write.append(line)
            elif timecode:
                to_write.append(line)
            elif line_break:
                pass
            else:
                next_slide, next_timecode, next_linebreak, next_text = test_line(cleaned_file, count + 1)
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
            slide, timecode, line_break, text = False, False, False, False
            next_slide, next_timecode, next_linebreak, next_text = False, False, False, False

    return to_write

def main(path, file):
    new_filename = clean_filename(file)
    file_path = path + file
    cleaned_file = linebreak_file(file_path)
    new_file = process_file(cleaned_file)
    fh.write_file(path, new_file, new_filename)
    return


if __name__ == '__main__':
    main()
