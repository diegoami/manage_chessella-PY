import tkinter as tk

import retrieve_from_chessbase as rfc;

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.fileLinkLabel= tk.Label(self)
        self.fileLinkLabel["text"] = "fileLink"
        self.fileLinkLabel.pack()

        self.fileLinkEntryBox = tk.Entry(self)
        self.fileLinkEntryBox.focus_set()
        self.fileLinkEntryBox.pack()



        self.executeButton = tk.Button(self)
        self.executeButton["text"] = "Retrieve pgns\n"
        self.executeButton["command"] = self.do_retrieve_pgns
        self.executeButton.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=root.destroy)
        self.quit.pack(side="bottom")

    def do_retrieve_pgns(self):

        rfc.retrieve_games(self.fileLinkEntryBox.get())

root = tk.Tk()
app = Application(master=root)
app.mainloop()