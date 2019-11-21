# Playlisy Maker Application
import tkinter as tk
from tkinter import filedialog
import re
import os
from lib import Playlist

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
        self.playlist = Playlist()

        self.create_import_button()
        self.create_quit_button()
        self.create_entry_field()
        self.create_display_field()
        self.create_export_button()

    def create_import_button(self):
        self.import_button = tk.Button(self.frame,
                                  text="Import Existing Playlist",
                                  command=lambda: self.import_existing())
        self.import_button.place(relx=0.01, rely=0.01, relwidth=0.5, relheight=0.1)

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
                                    font=('', 16))
        self.entry_title.place(relx=0, rely=0.15, relwidth=0.45, height=25)

        self.save_dir_title = tk.Label(self.frame,
                                       text="Select Save Location:",
                                       bg='#80c1ff',
                                       justify=tk.LEFT,
                                       anchor='w',
                                       font=('', 16))
        self.save_dir_title.place(relx=0, rely=0.3, relwidth=0.45, height=25)

        self.save_dir_browser = tk.Button(self.frame,
                                          text="Browse",
                                          command=lambda: self.browse_save_dir())
        self.save_dir_browser.place(relx=0, rely=0.35, width=80, height=30)


        self.save_dir = tk.StringVar(self)
        self.save_dir.set("Location to save your playlists")
        self.save_dir_label = tk.Label(self.frame,
                                       textvariable=self.save_dir,
                                       bg='#80c1ff',
                                       justify=tk.LEFT,
                                       anchor='w',
                                       font=('', 10))
        self.save_dir_label.place(x=90, rely=0.35, width=400)

    def create_display_field(self):
        self.plist_display = tk.Listbox(self.frame,
                                        width=20,
                                        height=20,
                                        justify='left',
                                        font=('',10))
        self.plist_display.pack(side='left', fill='y')
        self.plist_display.place(relx=0.55, rely=0.2,
                                 relwidth=0.45, relheight=0.6)

        self.scrollbar = tk.Scrollbar(self.plist_display, orient="vertical")
        self.scrollbar.config(command=self.plist_display.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.plist_display.config(yscrollcommand=self.scrollbar.set)

        self.plist_top_text = tk.Label(self.frame,
                                       anchor='w',
                                       justify='left',
                                       text="Songs List:",
                                       bg='#80c1ff',
                                       font=('', 16))
        self.plist_top_text.place(relx=0.55, rely=0.15)

        self.plist_add_song_button = tk.Button(self.frame,
                                               text="Add Songs",
                                               command=lambda: self.browse_songs())
        self.plist_add_song_button.place(relx=0.67, rely=0.04, relwidth=0.25, relheight=0.1)

        self.delete_selected_button = tk.Button(self.frame,
                                                text="Delete",
                                                command=lambda: self.remove_song(self.plist_display.curselection()))
        self.delete_selected_button.place(relx=0.55, rely=0.82, relwidth=0.18, relheight=0.05)
        self.delete_selected_button.config(state=tk.DISABLED)

        self.move_up_button = tk.Button(self.frame,
                                        text="⬆",
                                        command=lambda: self.move_song_up(self.plist_display.curselection()))
        self.move_up_button.place(relx = 0.75, rely=0.82, relwidth=0.05, relheight=0.05)
        self.move_up_button.config(state=tk.DISABLED)

        self.move_down_button = tk.Button(self.frame,
                                          text="⬇",
                                          command=lambda: self.move_song_down(self.plist_display.curselection()))
        self.move_down_button.place(relx = 0.82, rely=0.82, relwidth=0.05, relheight=0.05)
        self.move_down_button.config(state=tk.DISABLED)

        # buttons require a selected item to be enabled
        def on_select(event):
            self.delete_selected_button.config(state=tk.ACTIVE)
            self.move_up_button.config(state=tk.ACTIVE)
            self.move_down_button.config(state=tk.ACTIVE)

        self.plist_display.bind("<<ListboxSelect>>", on_select)

    def create_export_button(self):
        self.export_button = tk.Button(self.frame, text="Export", command=self.export)
        self.export_button.place(relx=0.05, rely=0.6, relwidth=0.4, relheight=0.25)
        self.export_button.configure(state=tk.DISABLED)
        # add an event to the save dir so that this button can be enabled once it is selected
        def on_select_save_dir(*args):
            if self.save_dir.get() != '' and os.path.exists(self.save_dir.get()):
                self.export_button.configure(state=tk.ACTIVE)
            else:
                self.export_button.configure(state=tk.DISABLED)
        self.save_dir.trace_add("write", on_select_save_dir)

    def import_existing(self):
        playlist_file = filedialog.askopenfilename(title="Select Playlist",
                                                   filetypes=(("Playlists", "*.m3u"), ("All files", "*.*")))
        if playlist_file:
            self.playlist.import_existing(playlist_file)
            # set the title
            self.entry.delete(0, tk.END)
            self.entry.insert(0, self.playlist.title)
            # set the save dir
            self.save_dir.set(os.path.abspath(os.path.join(os.path.dirname(playlist_file), os.sep)))

            # add songs to the display
            self.plist_display.delete(0, tk.END)
            for song in self.playlist.song_list:
                self.plist_display.insert('end', os.path.basename(song))

    def export(self):
        try:
            self.playlist.title, filename = self.get_pl_name()
            # debug print to view playlist
            print(self.playlist, flush=True)
            if self.save_dir.get():
                self.playlist.export(self.save_dir.get(), filename, overwrite=True)
        except Exception as e:
            print(e)

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
        if save_dir:
            self.save_dir.set(save_dir)

    def browse_songs(self):
        songs = filedialog.askopenfilenames(title="Select Songs",
                                            filetypes=(("MP3 files", "*.mp3"), ("All files", "*.*")))
        if songs:
            for song in songs:
                self.playlist.song_list.append(song)
                self.plist_display.insert('end', os.path.basename(song))

    def remove_song(self, index):
        if index:
            i = self.plist_display.index(index)
            if i < len(self.playlist.song_list) and i >= 0:
                del self.playlist.song_list[i]
                self.plist_display.delete(i)
                if i == len(self.playlist.song_list):
                    self.plist_display.selection_set(i-1)
                else:
                    self.plist_display.selection_set(i)
            else:
                print(f"Error: Can't remove element {i} from playlist.")

    def move_song_up(self, index):
        if index:
            i = self.plist_display.index(index)
            if i == 0:
                pass # alread at top, do nothing
            elif i < len(self.playlist.song_list) and i > 0:
                # somewhere in middle, swap up
                self.playlist.song_list[i], self.playlist.song_list[i-1] = self.playlist.song_list[i-1], self.playlist.song_list[i]
                temp = self.plist_display.get(i)
                self.plist_display.delete(i)
                self.plist_display.insert(i-1, temp)
                self.plist_display.selection_set(i-1)
            else:
                print(f"Error: Element {i} not in playlist.")

    def move_song_down(self, index):
        if index:
            i = self.plist_display.index(index)
            if i == len(self.playlist.song_list) - 1:
                pass # alread at bottom, do nothing
            elif i < len(self.playlist.song_list) - 1 and i >= 0:
                # somewhere in middle, swap up
                self.playlist.song_list[i], self.playlist.song_list[i+1] = self.playlist.song_list[i+1], self.playlist.song_list[i]
                temp = self.plist_display.get(i)
                self.plist_display.delete(i)
                self.plist_display.insert(i+1, temp)
                self.plist_display.selection_set(i+1)
            else:
                print(f"Error: Element {i} not in playlist.")


if __name__ == "__main__":
    root = tk.Tk()
    app = PlistMaker(master=root)
    app.mainloop()
