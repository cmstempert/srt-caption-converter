''' This module does two things:
        (1) Checks user input (a Directory from the File Dialog or file(s) from the
            Drag 'n Drop field) and returns them to the GUI for display if they are eligible for
            processing.
        (2) Saves processed text to new files.
'''

import os

# Function ensures data_path indicates that it is a directory
def filepath_format(data_path: str):
    ''' Takes filepath as string, adds / to the end if needed.
    '''
    try:
        if data_path[-1] != '/':
            data_path = data_path + '/'
        else:
            pass
    except IndexError:
        pass

    return data_path

# Function lists all files in given directory
def list_files(data_path: str):
    ''' Takes path to directory from file dialog as string. Returns list of all files in path.
    '''
    text_files = []

    for file in os.listdir(data_path):
        text_files.append(file)

    return text_files

# filters list to only include SRT files
def filter_filetypes(files_list: list):
    ''' Takes list of files (strings). Returns list of files with correct suffix (.srt).
    '''
    correct_formats = ['srt']
    good_files = []
    good_paths = []

    if type(files_list[0]) == str:
        for file in files_list:
            try:
                extension = file.strip().split(".")[1]

                if extension.lower() in correct_formats:
                    good_files.append(file)
            except IndexError:
                pass
    else:
        for file in files_list:
            try:
                extension = file[1].strip().split(".")[1]

                if extension.lower() in correct_formats:
                    good_files.append(file[1])
                    good_paths.append(file[0])
            except IndexError:
                pass

    return good_files, good_paths

def filter_formatted(files_list: list):
    ''' Takes list of files as strings and checks to see if their last 10 characters match the
        format declaration that would have been added if they were previously processed. Returns
        only files with filenames indicating no previous processing by this application.
    '''
    format_declaration = "-Formatted"
    new_flist = []
    new_plist = []

    try:
#        if type(files_list[0]) == str:
        for file in files_list:
            filename = file.strip().split(".")[0]

            if format_declaration != filename[-10:]:
                new_flist.append(file)
    except AttributeError:
#        else:
        for file in files_list:
            filename = file[1].strip().split(".")[0]

            if format_declaration != filename[-10:]:
                new_flist.append(file[1])
                new_plist.append(file[0])

    return new_flist, new_plist

# Function separates filename from path from singular input
def extract_path(input_list: list):
    ''' Takes list of file paths and splits the filename from the path. Returns separate lists of
        filenames and paths.
    '''
    path_list = []
    file_list = []

    for item in input_list:
        split = item.rsplit("/", 1)
        path_list.append(split[0])
        file_list.append(split[1])

    return path_list, file_list

# Function separates filepaths into a list after input as a single string
def split_filestring(stringlist: list):
    ''' Takes list of strings of one or more filepaths from the Drag 'n Drop field and
        splits them by distinct filepath. Returns list of filepaths .
    '''
    cleaned_list = []

    for item in stringlist:
        split = item.split("} {")
        cleaned_list.extend(split)

    for i, item in enumerate(cleaned_list):
        cleaned_list[i] = item.replace("{", "").replace("}", "")

    return cleaned_list

# Master function to process data taken in from DnD GUI interface
def dnd_file_strings(stringlist: list):
    ''' Takes list of strings from Drag 'n Drop field. Returns parallel lists of SRT filenames
        and their corresponding paths.
    '''
    clean_paths = []

    input_list = split_filestring(stringlist)
    path_list, file_list = extract_path(input_list)
    merged_list = list(map(lambda x, y: (x, y), path_list, file_list))
    good_files, good_paths = filter_filetypes(merged_list)
    good_merge = list(map(lambda x, y: (x, y), good_paths, good_files))
    new_srt_list, new_path_list = filter_formatted(good_merge)

    for path in new_path_list:
        result = filepath_format(path)
        clean_paths.append(result)

    return new_srt_list, clean_paths

# Master function to process data from SelectDirectory interface
def process_directory(dir_path: str):
    ''' Takes directory path from File Dialog. Returns list of SRT filenames and formatted
        directory path.
    '''
    if dir_path == '()':
        return [], dir_path

    formatted_path = filepath_format(dir_path)
    files_list = list_files(formatted_path)
    srt_list, _ = filter_filetypes(files_list)
    new_srt_list, _ = filter_formatted(srt_list)
    formatted_path = [formatted_path for x in new_srt_list]

    return new_srt_list, formatted_path

# write formatted contents to new file
def write_file(dir_path: str, text: list, new_filename: str):
    ''' Takes directory path and filename as strings and file text as a list. Writes and saves
        text to file in directory path.
    '''
    with open(dir_path + new_filename, 'w', encoding = "latin1") as f:

        for line in text:
            f.write(line)
            f.write("\n")

    f.close()

if __name__ == '__main__':
    process_directory()