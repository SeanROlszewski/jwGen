from jwGen import *
from Tkinter import *

MAX_HEIGHT = 250
MAX_WIDTH = 250

class JwGenApp(Frame):

    searchString = None


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

        self.button = Button(master, text="art", command=self.generateFromMouseEvent)
        self.button.grid(row=1, padx=frameWidth/10, pady=25)


    def generateFromKeyboardEvent(self, event):
        self.runJwGen(self.searchString.get())

    def generateFromMouseEvent(self):
        self.runJwGen(self.searchString.get())

    def runJwGen(self, string):
        jwGen(self.searchString.get())



if __name__ == '__main__':

    rootTk = Tk()
    rootTk.wm_attributes('-topmost', 1)
    rootTk.resizable(0,0)

    jwGenApp = JwGenApp(rootTk)
    jwGenApp.master.title("jwGen")
    jwGenApp.master.maxsize(MAX_HEIGHT, MAX_WIDTH)

    rootTk.mainloop()
