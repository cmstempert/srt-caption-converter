import customtkinter
from customtkinter import filedialog
import file_handler as fh
import text_processor as tp


# Creates label in scrollable frame
def FileFoundLabel(file, gridrow):
    label = customtkinter.CTkLabel(
        master = text_box,
        text = file)
    label.grid(row = gridrow, column = 0, sticky = "nsew")
    return

# Clears scrollable frame of all labels when 'Select' button is clicked
def ClearText():
    for widgets in text_box.winfo_children():
        widgets.destroy()

    file_label.configure(text = "Select a directory")
    return

# Function retrieves SRT file list, path, and calls function to create labels in scrollable frame
def FileSearch():
    global path
    global filtered_list
    gridrow = 0

    ClearText()

    path = r'{}'.format(filedialog.askdirectory(title = "Select Directory",
                    mustexist = True))
    
    filtered_list, path = fh.process_directory(path)

    ########################################################################
    ### NEED TO SEPARATE FILES THAT HAVE ALREADY BEEN PROCESSED FROM NEW ###
    ########################################################################

    # Creates on-screen labels for each file detected
    if len(filtered_list) > 0:
        FileFoundLabel("{} file(s) found".format(len(filtered_list)), gridrow)
        gridrow += 1

        for file in filtered_list:
            FileFoundLabel(file, gridrow)
            gridrow += 1
        
        process_btn.configure(state = "normal")
        file_label.configure(text = path)
    else:
        FileFoundLabel("No SRT files found", gridrow)
        process_btn.configure(state = "disabled")

    return

# Function creates 'completed' label for each file processed
def ProcessedLabel(gridrow):
    label = customtkinter.CTkLabel(
        master = text_box,
        text_color = "green",
        text = ".....Completed")
    label.grid(row = gridrow, column = 1, sticky = "nsew")
    return

# Function that calls text processor for each file in list and creates 'completed' label when done 
def ProcessFiles():
    row_count = 1
    process_btn.configure(state = "disabled")

    for file in filtered_list:
        tp.main(path, file)
        ProcessedLabel(row_count)
        row_count += 1    

    return


# Basic gui setup
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("600x300")
root.minsize(width = 580, height = 330)
root.maxsize(width = 580, height = 330)
root.title('SRT Caption Converter')
customtkinter.DrawEngine.preferred_drawing_method = "circle_shapes"

# Button for directory selection
select_btn = customtkinter.CTkButton(
    master = root,
    text = "Select",
    command = FileSearch,
    width = 60)
select_btn.place(x = 10, y = 10)

# Label with filler text before a directory/file is chosen
file_label = customtkinter.CTkLabel(
    master = root,
    text = "Select a directory",
    wraplength = 500)
file_label.place(x = 80, y = 10)

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
