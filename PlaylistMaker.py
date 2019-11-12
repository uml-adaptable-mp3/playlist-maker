# Playlisy Maker Application
import tkinter as tk

# CONSTANTS
APP_HEIGHT = 600
APP_WIDTH = 800


class PlistMaker(tk.Frame):
  def __init__(self, master=None):
    super().__init__(master)
    self.master = master
    self.pack()

    self.canvas = tk.Canvas(self.master, height=APP_HEIGHT, width=APP_WIDTH)
    self.canvas.pack()
    self.frame = tk.Frame(self.master, bg='#80c1ff', bd=5)
    self.frame.place(relx=0.5, rely=0, relwidth=1, relheight=1, anchor='n')

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
    self.quit.place(relx=0.8,rely=0.9, relwidth=0.2, relheight=0.1)

  def create_entry_field(self):
    self.entry = tk.Entry(self.frame)
    self.entry.place(relx=0, rely=0.2, relwidth=0.45, relheight=0.05)

  def create_display_field(self):
    self.plist_display = tk.Label(self.frame,
                                  anchor='nw',
                                  justify='left',
                                  text="Display MP3s here") 
    self.plist_display.place(relx=0.55, rely=0.2, relwidth=0.45, relheight=0.6)
  
  def say_hi(self):
    print("hello there")


root = tk.Tk()
app = PlistMaker(master=root)
app.mainloop()
