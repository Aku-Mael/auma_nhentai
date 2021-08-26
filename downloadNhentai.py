import os
import sys
import requests
from shutil import rmtree
from PIL import Image
from urllib.request import urlopen
from io import BytesIO
from nhentai import Hentai


HENTAI_PAGE = "https://nhentai.net/g/"
HENTAI_PICTURES = "https://i.nhentai.net/galleries/"


class DownloadHentai():

    def __init__(self, code):

        # Hentai information
        self.hentai = Hentai(code)
        self.hentai.loadData()
        self.hentai.analyzeData()
        self.mainURL = self.hentai.title + '/'
        
    def setUrl(self, url):
        self.mainURL = url + '/' + self.hentai.title + '/'

    def downloadHentai(self):
        try:
            rmtree(self.mainURL)
        except:
            pass

        os.mkdir(self.mainURL)
        pages = int(self.hentai.pages)
        for i in range(pages):
            num_page = str(i + 1)
            self.create_image(HENTAI_PICTURES + self.hentai.id + '/' + num_page, num_page)

    def create_image(self, pre_url, name):
        extensiones = [".jpg", ".png"]

        for ext in extensiones:
            url = pre_url + ext
            check = requests.get(url)

            if check.status_code != 404:
                data = urlopen(url).read()
                file = BytesIO(data)
                img = Image.open(file)
                
                img.save(self.mainURL + name + ext)
                return
                

        print("Image extension problem")
        return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(sys.argv[0] + " [-u] [C:/location] code")
        exit()
    elif len(sys.argv) > 2:
        try:
            int(sys.argv[3])
        except:
            print("Insert a code")
            exit()
            
        hentai = DownloadHentai(sys.argv[3])
        
        if len(sys.argv) == 4:
            if sys.argv[1] == "-u":
                hentai.setUrl(sys.argv[2])
                
        hentai.downloadHentai()
        
