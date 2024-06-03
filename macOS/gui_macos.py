'''
Core module for CaptionConverter. Creates gui application window and calls
file_handler and text_processor functionality at user prompting.
'''

import customtkinter
from customtkinter import filedialog
import file_handler_macos as fh
import text_processor_macos as tp


def found_file_label(file, gridrow):
    ''' Creates file label in text_box.
    '''
    label = customtkinter.CTkLabel(
        master = text_box,
        text = file)
    label.grid(row = gridrow, column = 0, sticky = "nsew")

def clear_text():
    ''' Clears all label from text_box.
    '''
    for widgets in text_box.winfo_children():
        widgets.destroy()

    multi_label.configure(text = "Select a directory")

def dir_search():
    ''' Takes path selected by user FileDialog then calls functions to filter
    for SRT files and render labels in text_box.
    '''
    global path
    global filtered_list
    gridrow = 0

    clear_text()

    path = r'{}'.format(filedialog.askdirectory(title = "Select Directory",
                    mustexist = True))

    filtered_list, path = fh.process_directory(path)

    if len(filtered_list) > 0:
        found_file_label("{} file(s) found".format(len(filtered_list)), gridrow)
        gridrow += 1

        for file in filtered_list:
            found_file_label(file, gridrow)
            gridrow += 1

        process_btn.configure(state = "normal")
        multi_label.configure(text = path)
    else:
        found_file_label("No SRT files found", gridrow)
        process_btn.configure(state = "disabled")

def processed_label(gridrow):
    ''' Creates 'Completed' label for processed files and appends to existing
    found_file_label in text_box 
    '''
    label = customtkinter.CTkLabel(
        master = text_box,
        text_color = "green",
        text = ".....Completed")
    label.grid(row = gridrow, column = 1, sticky = "nsew")

def process_files():
    ''' On 'Process Files' click, calls functions to process selected files and render
    'Completed' labels
    '''
    row_count = 1
    process_btn.configure(state = "disabled")

    for file in filtered_list:
        tp.main(path, file)
        processed_label(row_count)
        row_count += 1


# Core window display setup
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("600x300")
root.minsize(width = 580, height = 330)
root.maxsize(width = 580, height = 330)
root.title('SRT Caption Converter')
customtkinter.DrawEngine.preferred_drawing_method = "circle_shapes"

# Button for open file dialog window
select_btn = customtkinter.CTkButton(
    master = root,
    text = "Select",
    command = dir_search,
    width = 60)
select_btn.place(x = 10, y = 10)

# Label that displays path selected through file dialog window
multi_label = customtkinter.CTkLabel(
    master = root,
    text = "Select a directory",
    wraplength = 500)
multi_label.place(x = 80, y = 10)

# Button to trigger text processing operation
process_btn = customtkinter.CTkButton(
    master = root,
    text = "Process File(s)",
    width = 160,
    command = process_files,
    state = "disabled")
process_btn.place(x = 210, y = 60)

# Frame populated by selected files when detected
text_box = customtkinter.CTkScrollableFrame(
    master = root,
    width = 540)
text_box.place(x = 10, y = 100)


root.mainloop()
