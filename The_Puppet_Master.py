# _____________________________________________________________________________________________________________________
# There are some logos and pictures in the folder, they must be downloaded and put in the same folder that has the    |
# python file. Otherwise, the file won't have any logos or pictures but it will work perfectly.                       |
#                                                                                                                     |
# The main function of the application is to gather many files from many directories and edit them by either sorting  |
# them in a new folder or rename them fastly.                                                                         |
# ---------------------------------------------------------------------------------------------------------------------

from tkinter import *
from tkinter import ttk, messagebox, filedialog
import os
import shutil


# ----------------------------------------------------------------------------------------------------------------------
# setting up all the functions

def controller(window_name, master):  # controls the visibility of each window to the user
    try:
        if window_name == "workspace":
            mainWin.iconify()
            workspaceFun()
        elif window_name == "mainWin":
            master.destroy()
            mainWin.deiconify()
    except:
        messagebox.showerror("Something went wrong !!", "Something went wrong !!")


def how_to_use_it():  # display the contact window
    how_to = Toplevel(bg=lightBlue)
    how_to.title("How to use the app")
    how_to.geometry("600x520+340+80")
    how_to.resizable(0, 0)

    Label(how_to, text="How to use the app ?", bg=Blue, font=topic_font, padx=10, pady=10
          ).pack(side=TOP, fill=X, padx=10, pady=10)
    description = "You can sort and rename hundreds of files within few seconds.\n" \
                  "- Select files as much as you want from the adding window by browsing your disk from the first" \
                  " sub window. Or typing a path in the second one to add multiple files at once.\n" \
                  "- You can add folders in the other box (paths box) by their paths from the third sub window. So" \
                  " we can get to the files inside them.\n" \
                  "- You can sort the gathered files inside the items box. Just select the type of sorting and the " \
                  "new place for the sorted files then hit \"Sort\".\n" \
                  "- \"Sort\" button will take a copy of all files from BOTH boxes and paste it in the given " \
                  "folder.\n" \
                  "- Customized renaming is a one-by-one process. Select a file and type the new name then hit " \
                  " \"Rename\".\n" \
                  "- \"Quick Rename\" button will rename all files inside the selected path from the paths list " \
                  "as a sequence of numbers. Unless you want to \"Select all\" the paths and rename all the files " \
                  "inside each one of them."

    Label(how_to, text=description, bg=Blue, justify="left", wraplength=540, font=text_font, padx=10, pady=10
          ).pack(side=BOTTOM, fill=X, padx=10, pady=10)


def path_info():  # provide info about the meaning of the phrase "path" in case the user didn't know
    info = Toplevel(bg=Blue)
    info.title("What is the path ?")
    info.geometry("620x500+360+80")
    info.resizable(0, 0)
    Label(info, bg=lightBlue, font=text_font, text="The path is the sequence of folders that reaches a specific place "
                                                   "in the device").place(x=20, y=20)
    try:  # using "try" statement so if the logo files are not exist, the code doesn't crash
        Label(info, image=path1).place(x=20, y=50)
    except:
        Label(info, text="Picture is lost", font=text_font).place(x=100, y=100)
    Label(info, bg=lightBlue, font=text_font, text="Click this path and copy it ").place(x=20, y=240)
    try:
        Label(info, image=path2).place(x=20, y=270)
    except:
        Label(info, text="Picture is lost", font=text_font).place(x=100, y=320)
    Label(info, bg=lightBlue, font=text_font, text="Now just paste it in the field ").place(x=20, y=460)


def contact_me():
    contact = Toplevel(bg=lightBlue)
    contact.title("Contact me")
    contact.geometry("600x320+340+80")
    contact.resizable(0, 0)

    Label(contact, text="--- ENG. Mustfa Ayyed Alhasanat ---", bg=Blue, font=("Cooper Black", 20, "bold")
          , padx=20, pady=20).pack(side=TOP, fill=X, padx=20, pady=20)

    contents = Text(contact, width=50, bg=Blue, padx=20, pady=20, font=text_font)
    contents.pack(side=TOP, fill=X, padx=20, pady=20)
    txt = "e-mail >> mustfaaayyed@gmail.com\n" \
          "phone number >> +962 7 80387522\n" \
          "university >> TTU (Tafila Technical University)\n" \
          "specialty >> Communications and Electronics Engineering"
    contents.insert(INSERT, txt)


def sort(obj_listbox, paths_listbox, new_path_entry, combo_text):
    # response to the click on the "Sort" button by applying the selected orders
    try:
        if not obj_listbox.get(0, END) and not paths_listbox.get(0, END) and not new_path_entry.get():
            messagebox.showerror("Where are they ??", "At least one of the two boxes, and the new-path field mustn't be "
                                                      "empty.")
            new_path_entry.delete(0, END)
            return 0

        error_message = "You have to fill the path field with a valid path and select the type of " \
                        "sorting\n\nAlthough, you may have a file with the name \"The Organized Files\" in the given " \
                        "path. Please delete it and try again "
        done_message = "Congrats ... Mission has accomplished !!!\nYou can find your ORGANIZED files here :\n"

        # get all the items from the two boxes
        objects_dir, paths = list(obj_listbox.get(0, END)), list(paths_listbox.get(0, END))
        new_path = new_path_entry.get().replace("\\", "\\\\")

        items = []  # a list that will have all names of the files

        if not os.path.isdir(new_path):  # assure that the given path is valid
            messagebox.showerror("What was that ??", "Invalid path in the new-path field")
            new_path_entry.delete(0, END)
            return 0

        for path in paths:  # put all the files' directories with their names inside the list "objects_dir"
            os.chdir(path)
            dirs = os.listdir(path)
            for file in dirs:
                if (os.path.isdir(file)) or (file == "desktop.ini"):
                    continue
                objects_dir.append(f"{path}\\{file}")

        for item in objects_dir:
            items.append(item[len(os.path.dirname(item)) + 1:])  # add the names of the files

        # using "if" statement to check the selected choice inside the combo box that specifies the sorting type
        if combo_text.get() == "Sort by their names (alphabetically)":  # enter if it's an alphabetic sorting
            try:
                list_of_alpha = []  # a list that will have one of each letter from the given files
                marks_of_items = []  # a list that will have marks of letters for each item (so we can skip modifying
                # folders with no interfering with the list_of_alpha)

                for i, num in zip(items, range(len(items))):  # extract all the initial letters from the files
                    if os.path.isdir(objects_dir[num]):
                        marks_of_items.append("folder")
                        continue
                    first_letter = i[0]
                    list_of_alpha.append(first_letter)
                    marks_of_items.append(first_letter)

                list_of_alpha = list(set(list_of_alpha))  # delete all the duplicates
                new_path = new_path + "\\\\Organized By Names"
                os.mkdir(new_path)  # make the new folder that has it all
                os.chdir(new_path)

                for i in list_of_alpha:  # make a folder for each letter
                    try:
                        os.mkdir(new_path + f"\\\\{i}")
                    except:
                        pass

                # copy the old files and paste them in the new folders
                for i, c in zip(objects_dir, range(len(objects_dir))):
                    if marks_of_items[c] == "folder":
                        continue
                    os.chdir(new_path)
                    dest = new_path + f"\\\\{marks_of_items[c]}"
                    shutil.copy(i, dest)

                new_path_entry.delete(0, END)
                messagebox.showinfo("Congratulations", done_message + new_path)
            except:
                messagebox.showerror("What was that !!!", error_message)
                new_path_entry.delete(0, END)

        elif combo_text.get() == "Sort by their types (extensions)":  # enter if it's a type sorting
            try:
                list_of_exe = []  # a list that will have one of each extension
                marks_of_items = []  # a list that will have marks of extensions for each item

                for i in items:  # extract all the extensions from the files
                    if os.path.isdir(i):
                        marks_of_items.append("folder")
                        continue
                    name, exe = os.path.splitext(i)
                    list_of_exe.append(exe)
                    marks_of_items.append(exe)

                list_of_exe = list(set(list_of_exe))  # delete all the duplicates
                new_path = new_path + "\\\\Organized By Extensions"
                os.mkdir(new_path)  # create the new folder
                os.chdir(new_path)

                for i in list_of_exe:  # create a folder for each extension
                    os.mkdir(new_path + f"\\\\{i}")

                for i, c in zip(objects_dir, range(len(objects_dir))):  # copy and paste in the new folders
                    if marks_of_items[c] == "folder":
                        continue
                    os.chdir(new_path)
                    dest = new_path + f"\\\\{marks_of_items[c]}"
                    shutil.copy(i, dest)

                new_path_entry.delete(0, END)
                messagebox.showinfo("Congratulations", done_message + new_path)
            except:
                messagebox.showerror("What was that !!!", error_message)
                new_path_entry.delete(0, END)
        else:
            messagebox.showerror("What was that !!!", error_message)
            new_path_entry.delete(0, END)

    except:
        messagebox.showerror("Something went wrong !!", "Something went wrong !!")
        new_path_entry.delete(0, END)


def rename(entry, entry_text, listbox):  # response to the rename button
    try:
        item = listbox.get(ANCHOR)  # get the selected item
        name, exe = os.path.splitext(item[len(os.path.dirname(item)):])  # get the name and the extension of the item
        new_dir = f"{os.path.dirname(item)}{entry_text}{exe}"  # make the new path and name
        try:
            os.rename(item, new_dir)  # rename the item
            messagebox.showinfo("All done boss ;)", "File has been renamed successfully !!")
            listbox.delete(ANCHOR)  # clear the field
            entry.delete(0, END)
        except:
            messagebox.showerror("Really -_-", "You did not select any item to rename or the file you are trying to "
                                               "rename may not exist.")
            entry.delete(0, END)
    except:
        messagebox.showerror("Something went wrong !", "You did not select any item to rename or the file you are "
                                                       "trying to rename may not exist.")
        entry.delete(0, END)


def browse(master, browse_entry, listbox):  # response to clicking the "Browse" button (opens a dialog box to select a file from disk)
    try:
        browse_entry.delete(0, END)  # clear the entry's text
        master.filenames = filedialog.askopenfilenames(initialdir=r"C:", title="Select a file", filetypes=(("All", "*.*"), ("png file", "*png")))
        
        if len(master.filenames) == 1:  # if the user had selected only one file
            browse_entry.insert(0, master.filenames)  # insert the file inside the entry
        elif len(master.filenames) > 1:  # if the user had selected more than one file
            for item in master.filenames:
                add_item(item, listbox, browse_entry)  # add files to the list
    except:
        messagebox.showerror("Something went wrong !!", "Something went wrong !!")
        browse_entry.delete(0, END)


def add_item(item, listbox, entry):  # response to clicking the "Add" button in the first sub window inside the
    # notebook (adds the given file's name to the box of items)
    try:
        item = str(item).replace("/", "\\")

        if item in listbox.get(0, END):  # reject the existed items
            messagebox.showerror("Get something new o_o", "This item already exists in the list.")
            entry.delete(0, END)
            return 0

        elif not item:  # reject the empty field
            messagebox.showerror("Really -_-", "There are no items in the field")
            return 0

        dir_name = os.path.dirname(item)  # get the name of the path
        try:  # check if it was a valid path
            os.chdir(dir_name)
        except:
            messagebox.showerror("What was that !!", "Invalid path")
            entry.delete(0, END)
            return 0
        listbox.insert(END, item)  # add the item inside the box
        entry.delete(0, END)  # clear the field
        mainWin.iconify()

    except:
        messagebox.showerror("Something went wrong !!", "Something went wrong !!")
        entry.delete(0, END)  # clear the field


def add_list(path, listbox, entry, type_of_input):  # response to clicking the "add" button from the second and third sub window
    try:
        duplicate = False  # a mark for a file that is already exist in the list (it will be changed latter)

        if not path:  # reject the empty field
            messagebox.showerror("Really -_-", "There is no path in the field")
            entry.delete(0, END)
            return 0

        try:  # check if it was a valid path
            os.chdir(path)
        except:
            messagebox.showerror("Really -_-", "Invalid path")
            entry.delete(0, END)
            return 0

        if type_of_input == "path":  # a mark for the third sub window
            if path in listbox.get(0, END):  # reject the existed items
                messagebox.showerror("Get something new o_o",
                                     "There are some items in this path already exist in the list.\n"
                                     "Otherwise, any other new file should be added")
                entry.delete(0, END)
                return 0

            listbox.insert(END, f"{path}")  # insert the path
            entry.delete(0, END)
            return 0

        items = os.listdir(path)  # get a list of the contents of that path

        if not items:  # reject the empty path
            messagebox.showerror("Really -_-", "There are no items in that path")
            entry.delete(0, END)
            return 0

        for item in items:  # insert the items
            if f"{path}\\{item}" in listbox.get(0, END):  # reject the existed items
                duplicate = True
                continue
            if (os.path.isdir(item)) or (item == "desktop.ini"):  # reject folders
                continue
            listbox.insert(END, f"{path}\\{item}")

        if duplicate:  # raise an error only once for existed files instead of many times
            messagebox.showerror("Get something new o_o",
                                 "There are some items in this path already exist in the list.\n"
                                 "Otherwise, any other new file should be added")

        entry.delete(0, END)  # clear the field
        mainWin.iconify()

    except:
        messagebox.showerror("Something went wrong !!", "Something went wrong !!")
        entry.delete(0, END)  # clear the field


def delete(listbox, DEL):  # delete the selected item from the box, or delete them all if (DEL=True)
    if not DEL:
        if listbox.get(ANCHOR) != "":
            listbox.delete(ANCHOR)
        else:
            messagebox.showerror("Really -_-", "No item has been selected.")
    else:
        if not listbox.get(0, END):
            messagebox.showerror("Really -_-", "There are no items in the field.")


def entryGet(entry):  # return the text written inside the given Entry
    return entry.get()


def combo_check(combo_text):  # check the user's selection of the combobox beside the "sort" button
    if combo_text.get() == "Sort by their names (alphabetically)":
        messagebox.showinfo("Sort by their names", "Create several folders in the given path, One for each detected "
                                                   "alphabet letter. Then copy your files and distribute them among "
                                                   "those folders.")
    elif combo_text.get() == "Sort by their types (extensions)":
        messagebox.showinfo("Sort by their names", "Create several folders at the given path one for each detected "
                                                   "type. Then copy your files and distribute them among those "
                                                   "folders.")
    else:
        messagebox.showerror("Really -_-", "You have to select a sorting technique")


def quickRename(listbox, checkButtonVar):  # response to clicking the "Quick rename" button

    is_select_all = checkButtonVar.get()  # get the state of the check button
    error = False  # a mark for handling many errors in one time

    if not listbox.get(0, END):  # reject empty box
        messagebox.showerror("Really -_-", "The paths box is empty !!")
        return
    try:
        if not is_select_all:  # do this for only selected path (if they didn't check "select all")
            path = listbox.get(ANCHOR)

            for item, num in zip(os.listdir(path), range(len(os.listdir(path)))):  # rename all the files inside that path
                if (os.path.isdir(item)) or (item == "desktop.ini"):  # reject folders
                    continue
                name, exe = os.path.splitext(item)
                try:
                    os.rename(f"{path}\\{item}", f"{path}\\{num}{exe}")
                    listbox.delete(0, END)

                except:
                    error = True

            if error:
                messagebox.showerror("Something went wrong !", "One or more of the files you are trying to rename may "
                                                               "not exist. Otherwise, any other file should be "
                                                               "renamed successfully.")

        else:  # do this for all files in all paths inside the paths box (if they've checked "select all")
            paths = listbox.get(0, END)

            for path in paths:  # a loop for the paths and one for paths' files to rename all the files in all paths
                for item, num in zip(os.listdir(path), range(len(os.listdir(path)))):

                    if (os.path.isdir(item)) or (item == "desktop.ini"):  # reject folders
                        continue

                    name, exe = os.path.splitext(item)
                    new_dir = f"{path}\\{num}{exe}"
                    try:
                        os.rename(f"{path}\\{item}", new_dir)
                        listbox.delete(0, END)

                    except:
                        error = True

            if error:
                messagebox.showerror("Something went wrong !", "One or more of the files you are trying to rename may "
                                                               "not exist. Otherwise, any other file should be "
                                                               "renamed successfully.")
        messagebox.showinfo("All done boss ;)", "Files have been renamed successfully !!")

    except:
        messagebox.showerror("Something went wrong !", "You did not select any path to rename or one of the files "
                                                       "you are trying to rename may not exist.")


def select_all_Fun(var, checkButton):  # change the background color of the check-button when clicked
    if var.get() == 0:
        checkButton.config(bg="red")
    elif var.get() == 1:
        checkButton.config(bg="green")


# ----------------------------------------------------------------------------------------------------------------------
# workspace (the working window inside a function)
def workspaceFun():
    workspace = Toplevel(bg=lightBlue)
    workspace.title("The Puppet Master")
    workspace.geometry("812x650+260+20")
    workspace.resizable(0, 0)
    x_point, y_point = 15, 5

    try:
        workspace.iconbitmap("logo270.ico")
    except:
        pass

    # define the menu and the submenus
    mainMenu = Menu(workspace)
    fileMenu = Menu(mainMenu, bg=darkBlue, fg="#FFFFFF", font=("times", 13, "bold"))
    helpMenu = Menu(mainMenu, bg=darkBlue, fg="#FFFFFF", font=("times", 13, "bold"))

    mainMenu.add_cascade(label="File", menu=fileMenu)
    mainMenu.add_cascade(label="Help", menu=helpMenu)

    for master, label, command in zip([fileMenu, helpMenu, helpMenu, helpMenu], ["Exit", "How to use it ?", "What is the \"PATH\" ?", "Contact me"],
                                      [workspace.quit, how_to_use_it, path_info, contact_me]):
        master.add_command(label=label, command=command)

    workspace.config(menu=mainMenu)

    Button(workspace, text="Back", command=lambda: controller("mainWin", workspace), bg=Yellow, cursor="hand2",
           font=("Cooper Black", 20, "italic"), activebackground=darkBlue, activeforeground=Yellow).place(x=x_point+5, y=y_point+550)

    Label(workspace, text="CLick on the \"Help\" menu to learn how to use the app.", bg=Blue, fg="red", padx=7, pady=7,
          font=("Cooper Black", 14, "italic"), width=12, wraplength=150).place(x=x_point+120, y=y_point+500)

    Label(workspace, width=111, height=7, bg=Yellow).place(x=x_point, y=y_point+263)
    Label(workspace, width=111, height=5, bg=Yellow).place(x=x_point, y=y_point+385)

    # Notebook ---------------------------------------------------------------------------------------------------------
    Label(workspace, text="Add items and paths", bg=lightBlue, font=text_font).place(x=x_point, y=y_point)

    # define frames
    adding_ways = ttk.Notebook(workspace)
    adding_ways.place(x=x_point, y=y_point + 35)
    add_by_dir = Frame(adding_ways, bg=Blue)
    add_by_browse = Frame(adding_ways, bg=Blue)
    add_paths = Frame(adding_ways, bg=Blue)

    # draw the three sub windows in the notebook
    for master, text in zip([add_by_browse, add_by_dir, add_paths], ["-Add item/s-", "-Add multiple items-", "-Add a path-"]):
        adding_ways.add(master, text=text)

    # master : add_by_browse - first sub window (adding item/s)
    Label(add_by_browse, bg=Blue, height=12).pack(side=RIGHT, fill=Y)
    Label(add_by_browse, bg=Blue, width=38).pack(side=TOP, fill=X)
    for text, x, y, command in zip(["Add item/s by browsing your disk", "Add", "Delete", "Delete All"], [0, 20, 80, 160], [0, 120, 120, 120],
                                   [None, lambda: add_item(entryGet(filename_entry), objects_listbox, filename_entry),
                                        lambda: delete(objects_listbox, DEL=False), lambda: delete(objects_listbox, DEL=True)]):
        if x == 0:
            Label(add_by_browse, text=text, bg=Blue, font=text_font, width=26, justify="left").place(x=x, y=y)
            continue
        Button(add_by_browse, text=text, bg=Yellow, cursor="hand2", font=text_font, command=command).place(x=x, y=y)

    entry_var = StringVar()
    filename_entry = Entry(add_by_browse, textvariable=entry_var, font=("Consolas", 14, "bold"), bg=darkBlue, fg=Yellow, width=18)
    filename_entry.place(x=85, y=65)
    brose_button = Button(add_by_browse, text="Browse", font=text_font, fg=Yellow, bg=darkBlue, cursor="hand2")
    brose_button.place(x=5, y=60)

    # master : add_by_dir - second sub window (adding multiple items)
    Label(add_by_dir, text="Add multiple items by entering\ntheir path folder", bg=Blue, width=26, font=text_font, justify="left").place(x=0, y=0)
    entry_var2 = StringVar()
    filename_entry2 = Entry(add_by_dir, textvariable=entry_var2, font=("Consolas", 14, "bold"), fg=Yellow, bg=darkBlue, width=23)
    filename_entry2.place(x=15, y=65)

    for text, x, y, command in zip(["Add", "Delete", "Delete All"], [20, 80, 160], [120, 120, 120],
                                   [lambda: add_list(entryGet(filename_entry2), objects_listbox, filename_entry2, "files"),
                                    lambda: delete(objects_listbox, DEL=False), lambda: delete(objects_listbox, DEL=True)]):
        Button(add_by_dir, font=text_font, bg=Yellow, cursor="hand2", text=text, command=command).place(x=x, y=y)

    # master : add_paths - sub window (adding paths)
    Label(add_paths, text="Add a path of files", bg=Blue, width=26, font=text_font, justify="left").place(x=0, y=0)
    entry_var3 = StringVar()
    filename_entry3 = Entry(add_paths, textvariable=entry_var3, font=("Consolas", 14, "bold"), fg=Yellow, bg=darkBlue, width=23)
    filename_entry3.place(x=15, y=65)

    for text, x, y, command in zip(["Add", "Delete", "Delete All"], [20, 80, 160], [120, 120, 120],
                                   [lambda: add_list(entryGet(filename_entry3), paths_listbox, filename_entry3, "path"),
                                    lambda: delete(paths_listbox, DEL=False), lambda: delete(paths_listbox, DEL=True)]):
        Button(add_paths, font=text_font, bg=Yellow, cursor="hand2", text=text, command=command).place(x=x, y=y)

    # Added items listbox ----------------------------------------------------------------------------------------------
    Label(workspace, text="Added items", bg=lightBlue, font=text_font).place(x=x_point + 300, y=y_point)

    objects = PanedWindow(workspace)
    objects.place(x=x_point + 300, y=y_point + 35)
    objects_scrollbarY = Scrollbar(objects)
    objects_scrollbarY.pack(side=RIGHT, fill=Y)
    objects_scrollbarX = Scrollbar(objects, orient=HORIZONTAL)
    objects_scrollbarX.pack(side=BOTTOM, fill=X)
    objects_listbox = Listbox(objects, bg=Blue, width=35, height=12, yscrollcommand=objects_scrollbarY.set, xscrollcommand=objects_scrollbarX.set)
    objects_listbox.pack(side=LEFT, fill=Y)
    objects_scrollbarY.config(command=objects_listbox.yview)
    objects_scrollbarX.config(command=objects_listbox.xview)

    brose_button.config(command=lambda: browse(mainWin, filename_entry, objects_listbox))

    # Added paths listbox ----------------------------------------------------------------------------------------------
    Label(workspace, text="Added paths", bg=lightBlue, font=text_font).place(x=x_point + 550, y=y_point)

    paths = PanedWindow(workspace)
    paths.place(x=x_point + 550, y=y_point + 35)
    paths_scrollbarY = Scrollbar(paths)
    paths_scrollbarY.pack(side=RIGHT, fill=Y)
    paths_scrollbarX = Scrollbar(paths, orient=HORIZONTAL)
    paths_scrollbarX.pack(side=BOTTOM, fill=X)
    paths_listbox = Listbox(paths, bg=Blue, width=35, height=12, yscrollcommand=paths_scrollbarY.set, xscrollcommand=paths_scrollbarX.set)
    paths_listbox.pack(side=LEFT, fill=Y)
    paths_scrollbarY.config(command=paths_listbox.yview)
    paths_scrollbarX.config(command=paths_listbox.xview)

    # selection area ---------------------------------------------------------------------------------------------------
    new_path, new_name = StringVar(), StringVar()

    Label(workspace, text="Enter the path where you want to save the new files then \nchoose the type of sorting "
                          "(by extensions or by names) \n(Only if you want to resort them in a new folder)",
          font=text_font, bg=Yellow).place(x=x_point, y=y_point + 270)

    new_path_field = Entry(workspace, textvariable=new_path, width=18, bg=darkBlue, fg=Yellow, insertbackground=Blue, font=("Consolas", 15, "bold"))
    new_path_field.place(x=x_point + 460, y=y_point + 275)

    combo_text = StringVar()
    combo_values = ("Sort by their names (alphabetically)", "Sort by their types (extensions)")
    ttk.Combobox(workspace, textvariable=combo_text, values=combo_values, width=30).place(x=x_point + 460, y=y_point + 310)

    Label(workspace, text="Explain to me what will happen", bg=Yellow, font=text_font).place(x=x_point + 450, y=y_point + 340)
    Label(workspace, text="Enter the new name of the selected file here :", font=text_font, bg=Yellow).place(x=x_point, y=y_point + 410)

    Button(workspace, activebackground=Yellow, bitmap="info", width=20, activeforeground=darkBlue, bg=darkBlue, fg=Yellow,
            command=lambda: combo_check(combo_text), font=text_font, cursor="hand2").place(x=x_point + 705, y=y_point + 340)
    Button(workspace, text="Sort", command=lambda: sort(objects_listbox, paths_listbox, new_path_field, combo_text), bg=darkBlue,
           font=("Cooper Black", 20), bd=4, relief=GROOVE, activebackground=Yellow, cursor="hand2", fg=Yellow,
           activeforeground=darkBlue).place(x=x_point + 680, y=y_point + 275)
    Button(workspace, text="Rename", bg=darkBlue, font=("Cooper Black", 18), bd=4, relief=GROOVE, fg=Yellow,
           activebackground=Yellow, cursor="hand2", activeforeground=darkBlue,
           command=lambda: rename(new_name_field, entryGet(new_name_field), objects_listbox)).place(x=x_point + 640, y=y_point + 400)

    new_name_field = Entry(workspace, textvariable=new_name, width=22, bg=darkBlue, fg=Yellow, insertbackground=Blue, font=("Consolas", 15, "bold"))
    new_name_field.place(x=x_point + 370, y=y_point + 412)

    # label frame (quick rename box) -----------------------------------------------------------------------------------
    quick_rename = LabelFrame(workspace, text="Quick Rename", bg=Blue, font=("Cooper Black", 15))
    quick_rename.place(x=x_point+312, y=y_point + 485)

    Label(quick_rename, text="Select a path from the paths box then click on the button (or you can check \"Select all\")",
          font=text_font, bg=Blue, width=25, justify="left", wraplength=230).pack(side=LEFT, fill=Y, padx=10, pady=3)

    select_all_var = IntVar()
    select_all = Checkbutton(quick_rename, text="Select all", font=text_font, bg="red", cursor="hand2",
                             variable=select_all_var, command=lambda: select_all_Fun(select_all_var, select_all))
    select_all.pack(side=BOTTOM, anchor="ne", padx=5, pady=5)

    Button(quick_rename, text="Quick Rename", bg=Yellow, font=("Cooper Black", 15), bd=4, relief=GROOVE, fg=darkBlue,
           activebackground=darkBlue, cursor="hand2", activeforeground=Yellow,
           command=lambda: quickRename(paths_listbox, select_all_var)).pack(side=TOP, anchor="se", padx=5, pady=5)


# ----------------------------------------------------------------------------------------------------------------------
# the main window
mainWin = Tk()
mainWin.title("The Puppet Master")
mainWin.geometry("385x650+450+20")
mainWin.resizable(0, 0)
mainWin.lift()

try:
    mainWin.iconbitmap("logo270.ico")
except:
    pass

lightBlue, Blue, darkBlue, Yellow = "#a2d5f2", "#40a8c4", "#07689f", "#ffc93c"
topic_font, text_font, logos_list = ("Cooper Black", 17, "underline"), ("Andalus", 12, "bold"), ["logo270.png", "1.png", "2.png"]

mainWin.config(bg=lightBlue)

#  putting the logo defining code in a try-statement so the code wont crash if the logos have lost
try:
    mainLogo, path1, path2 = PhotoImage(file=logos_list[0]), PhotoImage(file=logos_list[1]), PhotoImage(file=logos_list[2])
except:
    messagebox.showwarning("Where are the logos ???", "We can't find some of the logos in the project's folder !!!")

the_puppet_master_paned = PanedWindow(mainWin, bg=lightBlue)
the_puppet_master_paned.place(x=20, y=20)
Label(the_puppet_master_paned, text="The Puppet \nMaster", font=("Old English Text MT", 35), bg=lightBlue, width=11,
      padx=5, pady=5).pack(side=TOP, fill=X)

try:
    Label(the_puppet_master_paned, image=mainLogo, bg=lightBlue, padx=5, pady=5).pack(fill=X)
except:
    Label(the_puppet_master_paned, text="Logo is lost", bg=Blue, padx=5, pady=5).pack(fill=X)

Button(the_puppet_master_paned, text="Start", bg=Yellow, font=("Cooper Black", 20, "italic"), pady=5, cursor="hand2",
       activebackground=darkBlue, activeforeground=Yellow, command=lambda: controller("workspace", mainWin)).pack(side=BOTTOM, pady=5)

Label(the_puppet_master_paned, text="Manipulate files easily", font=("Andalus", 25, "bold"), bg=lightBlue, padx=5, pady=5).pack(side=BOTTOM, fill=X)

Label(mainWin, text="ENG. Mustfa Ayyed Alhasanat", height=1, font=("Cooper Black", 15, "italic"), bg=Blue).place(x=35, y=590)

# ----------------------------------------------------------------------------------------------------------------------
mainWin.mainloop()
