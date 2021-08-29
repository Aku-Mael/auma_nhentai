from tkinter import Tk
from tkinter import *
from nhentai import Hentai
from downloadNhentai import DownloadHentai
from nhentai import ConnectionErrorNHentai

class App:

    def __init__(self, root):
        self.window = root
        self.window.title("NHentai")
        self.window.geometry("500x280")
        self.window.resizable(False, False)
        
        # Important elements
        self.hentai = None
        self.icon = None
        self.iconFrame = LabelFrame(self.window)
        
        self.searchFrame = LabelFrame(self.window, text = "Enter the code")
        self.codeInput = None
        self.searchButtom = None
        self.downloadButtom = None
        
        self.infoWindow = None
        self.infoFrame = None
        self.infoLabel = None
        
        self.iconFrame.grid(row = 0, column = 0, padx = 10, pady = 10)
        self.searchFrame.grid(row = 0, column = 2, pady = 0, sticky=N)
        self.loadIcon()
        self.loadSearch()
        
        
    def loadIcon(self):
        try:
            self.icon = PhotoImage(file="resources/nhentai.png")
            widgetIcon = Label(self.iconFrame, image=self.icon)
        except TclError as e:
            print(e)
            widgetIcon = Label(self.iconFrame, text = "Error loading resource 'resources/nhentai2.png'")
        widgetIcon.pack()

    def loadSearch(self):
        self.codeInput = Entry(self.searchFrame)
        self.codeInput.focus()
        self.codeInput.grid(row = 1, column = 1)
        
        self.searchButtom = Button(self.searchFrame, text = "Search", command=self.search)
        self.searchButtom.grid(row = 3, columnspan=2, sticky=W + E)
        self.downloadButtom = Button(self.searchFrame, text = "Download", command=self.download)
        self.downloadButtom.grid(row = 4, columnspan=2, sticky=W + E)
        self.downloadButtom["state"] = DISABLED
        self.message = Label(self.searchFrame, text = "", fg='red')
        self.message.grid(row = 2, columnspan=2, sticky=W + E)
        
    def download(self):
        self.hentai.downloadHentai()
        self.downloadButtom.config(text="Download")
        self.downloadButtom["state"] = DISABLED
        
    def search(self):
        if self.validate():
            self.message.config(text='')
            self.hentai = DownloadHentai(self.codeInput.get())

            try:
                self.hentai.loadData()
            except ConnectionErrorNHentai as error:
                print(error)
                self.message.config(text=str(error))
                self.codeInput.delete(0, END)
                return
            self.hentai.analyzeData()
            self.showInfo()
            
            
    def validate(self):
        if len(self.codeInput.get()) != 0:
            try:
                int(self.codeInput.get())
            except Exception as e:
                self.message.config(text='That is not a code')
                self.codeInput.delete(0, END)
                return False
            return True
        else:
            self.message.config(text='Enter a code')
            self.codeInput.delete(0, END)
            return False        
        


    def showInfo(self):
        self.infoWindow = Toplevel()
        self.infoWindow.title(str(self.hentai.title))
        
        self.infoFrame = LabelFrame(self.infoWindow)
        self.infoFrame.grid(row = 0, column = 0, columnspan = 3, pady = 10)
        
        self.loadHentai()
        
        self.infoWindow.transient(master=self.window)
        self.infoWindow.grab_set()
        self.window.wait_window(self.infoWindow)
        self.downloadButtom["state"] = NORMAL
        string = "Download (Code: " + self.codeInput.get() + ")"
        self.downloadButtom.config(text=string)
        
    def loadHentai(self):
        data = {}
        if self.hentai.title:
            data["Title"] = self.hentai.title
        if self.hentai.pages:
            data["Pages"] = self.hentai.pages
            
        self.loadAttributes(self.hentai.parodies, "Parodies", data)
        self.loadAttributes(self.hentai.characters, "Characters", data)
        self.loadAttributes(self.hentai.tags, "Tags", data)
        self.loadAttributes(self.hentai.artists, "Artists", data)
        self.loadAttributes(self.hentai.groups, "Groups", data)
        self.loadAttributes(self.hentai.languages, "Languages", data)
        self.loadAttributes(self.hentai.categories, "Categories", data)
        
        string = ''
        for key in data.keys():
            strData = str(data[key]).replace("'","").replace("[","").replace("]","")
            string = string + key + " : " + strData + "\n"
        
        self.infoLabel = Label(self.infoFrame, text = string)
        self.infoLabel.grid(row = 2, columnspan=2, sticky=W + E)

    def loadAttributes(self, atributes, key, data):
        if atributes:
            data[key] = []
            for atribute in atributes:
                data[key].append(atribute)

if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()
