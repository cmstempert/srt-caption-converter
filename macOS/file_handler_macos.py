''' This module does two things:
        (1) Checks user input (a Directory from the File Dialog) and returns
            them to the GUI for display if they are eligible for processing.
        (2) Saves processed text to new files.
'''

import os

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

def list_files(data_path: str):
    ''' Takes path to directory from file dialog as string. Returns list of all files in path.
    '''
    text_files = []

    for file in os.listdir(data_path):
        text_files.append(file)

    return text_files

def filter_filetypes(files_list: list):
    ''' Takes list of files (strings). Returns list of files with correct suffix (.srt).
    '''
    correct_formats = ['srt']
    good_list = []

    for file in files_list:
        try:
            extension = file.strip().split(".")[1]

            if extension.lower() in correct_formats:
                good_list.append(file)
        except IndexError:
            pass

    return good_list

def filter_formatted(files_list: list):
    ''' Takes list of files as strings and checks to see if their last 10 characters match the
        format declaration that would have been added if they were previously processed. Returns
        only files with filenames indicating no previous processing by this application.
    '''
    format_declaration = "-Formatted"
    new_list = []

    for file in files_list:
        filename = file.strip().split(".")[0]

        if format_declaration != filename[-10:]:
            new_list.append(file)

    return new_list

def process_directory(dir_path: str):
    ''' Takes directory path from File Dialog. Returns list of SRT filenames and formatted
        directory path.
    '''
    if dir_path == '()':
        return [], dir_path

    formatted_path = filepath_format(dir_path)
    files_list = list_files(formatted_path)
    srt_list = filter_filetypes(files_list)
    new_srt_list = filter_formatted(srt_list)
    return new_srt_list, formatted_path

def write_file(dir_path: str, text: list, new_filename: str):
    ''' Takes directory path and filename as strings and file text as a list. Writes and saves
        text to file in directory path.
    '''
    with open(dir_path + new_filename, 'w', encoding='latin1') as f:

        for line in text:
            f.write(line)
            f.write("\n")

    f.close()


if __name__ == '__main__':
    process_directory()
