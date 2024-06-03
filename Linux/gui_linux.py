import customtkinter
from customtkinter import filedialog
from tkinterdnd2 import DND_FILES
import file_handler_linux as fh
import text_processor_linux as tp


# Creates label in scrollable frame
def file_found_label(file, gridrow):
    label = customtkinter.CTkLabel(
        master = text_box,
        text = file)
    label.grid(row = gridrow, column = 0, sticky = "nsew")

# Clears scrollable frame of all labels when 'Select' button is clicked
def clear_text():
    for widgets in text_box.winfo_children():
        widgets.destroy()

    multi_label.configure(text = "Select a directory")

def radio_action():
    value = radio_var.get()

    if value == "Select Directory":
        dnd_label.place_forget()
        select_btn.place(x = 140, y = 18)
        multi_label.place(x = 220, y = 18)
    else:
        select_btn.place_forget()
        multi_label.place_forget()
        dnd_label.place(x = 140, y = 18)

# Creates on-screen labels for each valid file detected
def populate_file_labels(filtered_list, path):
    gridrow = 0

    if len(filtered_list) > 0:
        file_found_label("{} file(s) found".format(len(filtered_list)), gridrow)
        gridrow += 1

        for file in filtered_list:
            file_found_label(file, gridrow)
            gridrow += 1

        process_btn.configure(state = "normal")
        multi_label.configure(text = path[0])
    else:
        file_found_label("No SRT files found", gridrow)
        process_btn.configure(state = "disabled")

def file_drop(event):
    global path_list
    global filtered_list

    dnd_list.append(event.data)
    filtered_list, path_list = fh.dnd_file_strings(dnd_list)
    populate_file_labels(filtered_list, path_list)

"""
Function retrieves file list from directory, path, and calls
function to create labels in scrollable frame
"""
def dir_search():
    global path_list
    global filtered_list

    clear_text()

    path = r'{}'.format(filedialog.askdirectory(title = "Select Directory",
                    mustexist = True))

    filtered_list, path_list = fh.process_directory(path)
    populate_file_labels(filtered_list, path_list)

# Function creates 'completed' label for each file processed
def processed_label(gridrow):
    label = customtkinter.CTkLabel(
        master = text_box,
        text_color = "green",
        text = ".....Completed")
    label.grid(row = gridrow, column = 1, sticky = "nsew")

# Function that calls text processor for each file in list and creates 'completed' label when done
def ProcessFiles():
    row_count = 1
    process_btn.configure(state = "disabled")

    for i, file in enumerate(filtered_list):
        tp.main(path_list[i], file)
        processed_label(row_count)
        row_count += 1

    dnd_list = []

# Basic gui setup
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("600x300")
root.minsize(width = 580, height = 330)
root.maxsize(width = 580, height = 330)
root.title('SRT Caption Converter')
customtkinter.DrawEngine.preferred_drawing_method = "circle_shapes"

# Label with filler text before a directory/file is chosen
multi_label = customtkinter.CTkLabel(
    master = root,
    text = "Select a directory",
    wraplength = 375)

# Button for directory selection
select_btn = customtkinter.CTkButton(
    master = root,
    text = "Select",
    command = dir_search,
    width = 60
    )

dnd_list = []
radio_var = customtkinter.StringVar(value="Drag & Drop")
operation_qty = ["Drag & Drop", "Select Directory"]

# Radio button for single file operation
radio_btn1 = customtkinter.CTkRadioButton(
    master = root,
    text = operation_qty[0],
    value = operation_qty[0],
    variable = radio_var,
    radiobutton_width = 18,
    radiobutton_height = 18,
    command = radio_action
)
radio_btn1.place(x = 10, y = 10)

# Radio button for multiple file operations
radio_btn2 = customtkinter.CTkRadioButton(
    master = root,
    text = operation_qty[1],
    value = operation_qty[1],
    variable = radio_var,
    radiobutton_width = 18,
    radiobutton_height = 18,
    command = radio_action
)
radio_btn2.place(x = 10, y = 32)

# Drag & Drop field
dnd_label = customtkinter.CTkLabel(
    master = root,
    text = "Drag & Drop Here",
    width = 300,
    fg_color = "gray15"
    )
dnd_label.drop_target_register(DND_FILES)
dnd_label.dnd_bind('<<Drop>>', file_drop)
dnd_label.place(x = 140, y = 18)

# Button to trigger text processing operation
process_btn = customtkinter.CTkButton(
    master = root,
    text = "Process File(s)",
    width = 160,
    command = ProcessFiles,
    state = "disabled")
process_btn.place(x = 210, y = 60)

# Frame populated by selected files when detected
text_box = customtkinter.CTkScrollableFrame(
    master = root,
    width = 540)
text_box.place(x = 10, y = 100)


root.mainloop()
