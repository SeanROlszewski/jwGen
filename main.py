from jwGen import *
from Tkinter import *
from multiprocessing import Process
import pdb

MAX_HEIGHT = 250
MAX_WIDTH = 250

class App(Frame):

    searchString = None

    def generateFromKeyboardEvent(self, event):
        jwGen(self.searchString.get())


    def generateFromMouseEvent(self):
        jwGen(self.searchString.get())


    def __init__(self, master):

        master.protocol("WM_DELETE_WINDOW", master.destroy)

        self.searchString = StringVar()

        Frame.__init__(self, master)
        self.config(height=MAX_HEIGHT, width=MAX_WIDTH)

        frameHeight = self.cget("height")
        frameWidth = self.cget("width")

        self.searchEntry = Entry(master, textvariable=self.searchString)
        self.searchEntry.bind("<Return>", self.generateFromKeyboardEvent)
        self.searchEntry.grid(row=0, padx=frameWidth/10, pady=10)

        self.button = Button(master, text="Generate", command=self.generateFromMouseEvent)
        self.button.grid(row=1, padx=frameWidth/10, pady=25)


if __name__ == '__main__':

    rootTk = Tk()
    rootTk.wm_attributes('-topmost', 1)
    app = App(rootTk)
    app.master.title("jwGen Version 0.1")
    app.master.maxsize(MAX_HEIGHT, MAX_WIDTH)

    rootTk.mainloop()
