# Playlisy Maker Application
import tkinter as tk
from tkinter import filedialog
import re
import os

# CONSTANTS
APP_HEIGHT = 600
APP_WIDTH = 800


class PlistMaker(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        self.master.iconbitmap('images/uml_logo.ico')

        self.canvas = tk.Canvas(self.master,
                                height=APP_HEIGHT,
                                width=APP_WIDTH)
        self.canvas.pack()
        self.frame = tk.Frame(self.master, bg='#80c1ff', bd=5)
        self.frame.place(relx=0.5, rely=0, relwidth=1, relheight=1, anchor='n')

        self.winfo_toplevel().title("AMP3 Playlist Maker")

        self.create_hello_button()
        self.create_quit_button()
        self.create_entry_field()
        self.create_display_field()

    def create_hello_button(self):
        self.hi_there = tk.Button(self.frame,
                                  text="Hello World",
                                  command=lambda: self.say_hi())
        self.hi_there.place(relx=0.01, rely=0.01, relwidth=0.5, relheight=0.1)

    def create_quit_button(self):
        self.quit = tk.Button(self.frame,
                              text="QUIT",
                              fg="red",
                              command=lambda: self.master.destroy())
        self.quit.place(relx=0.8, rely=0.9, relwidth=0.2, relheight=0.1)

    def create_entry_field(self):
        self.entry = tk.Entry(self.frame)
        self.entry.place(relx=0, rely=0.2, relwidth=0.45, height=25)

        self.entry_title = tk.Label(self.frame,
                                    text="Enter Playlist Name:",
                                    bg='#80c1ff',
                                    justify=tk.LEFT,
                                    anchor='w',
                                    font=20)
        self.entry_title.place(relx=0, rely=0.15, relwidth=0.45, height=25)

        self.save_dir_browser = tk.Button(self.frame,
                                          text="Browse",
                                          command=lambda: self.browse_save_dir())
        self.save_dir_browser.place(relx=0, rely=0.3, width=80, height=30)

        self.save_dir = tk.StringVar(self)
        self.save_dir.set("Location to save your playlists")
        self.save_dir_label = tk.Label(self.frame,
                                       textvariable=self.save_dir,
                                       bg='#80c1ff',
                                       justify=tk.LEFT,
                                       anchor='w',
                                       font=('',10))
        self.save_dir_label.place(x=90, rely=0.3, width=400)

    def create_display_field(self):
        self.plist_display = tk.Label(self.frame,
                                      anchor='nw',
                                      justify='left',
                                      text="Display MP3s here")
        self.plist_display.place(
            relx=0.55, rely=0.2, relwidth=0.45, relheight=0.6)

    def say_hi(self):
        print("hello there")
        print(self.get_pl_name())

    def get_pl_name(self):
        from_entry = self.entry.get()
        from_entry = from_entry.strip()
        # Remove all non-word characters (everything except numbers and letters)
        plain_entry = re.sub(r"[^\w\s-]", '', from_entry)
        # Replace all runs of whitespace with a single dash
        filename = re.sub(r"\s+", '_', plain_entry)
        filename = os.path.join(filename + ".m3u")
        return (plain_entry, filename)
    
    def browse_save_dir(self):
        save_dir = filedialog.askdirectory(title="Select Folder")
        self.save_dir.set(save_dir)


root = tk.Tk()
app = PlistMaker(master=root)
app.mainloop()
