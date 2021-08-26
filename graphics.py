from tkinter import Tk
from tkinter import *
from nhentai import Hentai
from downloadNhentai import DownloadHentai

class App:

    def __init__(self, root):
        self.window = root
        self.window.title("NHentai")
        self.window.geometry("500x280")
        self.window.resizable(False, False)
        self.hentai = None

        # Icono
        icon_frame = LabelFrame(self.window)
        icon_frame.grid(row = 0, column = 0, padx = 10, pady = 10)
        self.icon = PhotoImage(file="resources/nhentai.png")
        widget_icon = Label(icon_frame, image=self.icon).pack()
        
        
        search_frame = LabelFrame(self.window, text = "Enter the code")
        search_frame.grid(row = 0, column = 2, pady = 0, sticky=N)
        
        self.code = Entry(search_frame)
        self.code.focus()
        self.code.grid(row = 1, column = 1)
        
        self.search = Button(search_frame, text = "Search", command=self.search)
        self.search.grid(row = 3, columnspan=2, sticky=W + E)
        self.download = Button(search_frame, text = "Download", command=self.download)
        self.download.grid(row = 4, columnspan=2, sticky=W + E)
        self.download["state"] = DISABLED
        
        self.message = Label(search_frame, text = "", fg='red')
        self.message.grid(row = 2, columnspan=2, sticky=W + E)
        
        
        
    def validate(self):
        if len(self.code.get()) != 0:
            try:
                int(self.code.get())
            except Exception as e:
                self.message.config(text='That is not a code')
                self.code.delete(0, END)
                return False
            return True
        else:
            self.message.config(text='Enter a code')
            self.code.delete(0, END)
            return False        
        
    def search(self):
        if self.validate():
            self.message.config(text=' ')
            self.hentai = Hentai(self.code.get())
            if not self.hentai.loadData():
                self.message.config(text='Search error')
                self.code.delete(0, END)
                return
            self.hentai.analyzeData()
            self.downloadHentai = DownloadHentai(self.hentai)
            self.show_info()
            

    def show_info(self):
        self.info = Toplevel()
        self.info.title(str(self.hentai.title))
        self.info.resizable(False, False)
        
        info_frame = LabelFrame(self.info)
        info_frame.grid(row = 0, column = 0, columnspan = 3, pady = 10)
        info = Label(info_frame, text = str(self.hentai))
        info.grid(row = 2, columnspan=2, sticky=W + E)
        
        self.info.transient(master=self.window)
        self.info.grab_set()
        self.window.wait_window(self.info)
        self.download["state"] = NORMAL
        self.search["state"] = DISABLED
        
    def download(self):
        self.downloadHentai.downloadHentai()
        self.download["state"] = DISABLED
        self.search["state"] = NORMAL



if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()
