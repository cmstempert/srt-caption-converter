import os

# Function ensures data_path indicates that it is a directory
def filepath_format(data_path):
    try:    
        if data_path[-1] != '/':
            data_path = data_path + '/'
        else:
            pass
    except IndexError:
        pass

    return data_path

# Function lists all files in given directory
def list_files(data_path):
    text_files = []

    for file in os.listdir(data_path):
        text_files.append(file)
    
    return text_files

# filters list to only include SRT files
def filter_filetypes(files_list):
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

# Function filters out previously formatted SRT files based on filename
# containing tag appended by previous operation
def filter_formatted(files_list):
    format_declaration = "-Formatted"
    new_list = []

    for file in files_list:
        filename = file.strip().split(".")[0]

        if format_declaration != filename[-10:]:
            new_list.append(file)
    
    return new_list

# call list_files and filter_filetypes
def process_directory(dir_path):
    if dir_path == '()':
        return [], dir_path
    
    formatted_path = filepath_format(dir_path)
    files_list = list_files(formatted_path)
    srt_list = filter_filetypes(files_list)
    new_srt_list = filter_formatted(srt_list)
    return new_srt_list, formatted_path

# write formatted contents to new file 
def write_file(dir_path, text, new_filename):
    with open(dir_path + new_filename, 'w') as f:

        for line in text:
            f.write(line)
            f.write("\n")

    f.close()
    return

if __name__ == '__main__':
    process_directory()
