import os
import sys
import requests
from shutil import rmtree
from PIL import Image
from urllib.request import urlopen
from io import BytesIO
from nhentai import Hentai, ConnectionErrorNHentai


HENTAI_PAGE = "https://nhentai.net/g/"
HENTAI_PICTURES = "https://i.nhentai.net/galleries/"
COVER_PAGE = "https://t.nhentai.net/galleries/"


class DownloadHentai(Hentai):

    def __init__(self, code):

        super().__init__(code)
        # Hentai information
        self._directory = None
        self._troubledPages = []
        
    @property
    def directory(self):
        return self._directory

    @property
    def troubledPages(self):
        return self._troubledPages

    def setDirectory(self, url):
        self._directory = url + '/' + self.title + '/'

    def downloadHentai(self):

        if self._directory is None:
            self._directory = self.title + '/'

        try:
            rmtree(self._directory)
            print('Delete folder "' + self._directory + '"')
        except FileNotFoundError:
            pass

        os.mkdir(self._directory)
        pages = int(self.pages)
        for i in range(pages):
            num_page = str(i + 1)
            self.create_image(HENTAI_PICTURES + self.id + '/' + num_page, num_page)
        return True

    def create_image(self, pre_url, name):
        extensiones = [".jpg", ".png"]

        for ext in extensiones:
            url = pre_url + ext
            check = requests.get(url)

            if check.status_code != 404:
                data = urlopen(url).read()
                file = BytesIO(data)
                img = Image.open(file)
                img.save(self._directory + name + ext)
                return

        self._troubledPages.append(name)
        return None

    def __str__(self):
        string = "\nHentai info:\n" + str(super().__str__())
        string = string + "\n\nDownload Properties:"
        if self._directory:
            string = string + '\nURL: ' + self._directory
        if self._troubledPages:
            string = string + '\nTrouble Pages ' + str(self._troubledPages)
        return string


def downloadHentai(code):
    try:
        int(code)
    except ValueError:
        print("Write a code")
        return

    hentai = DownloadHentai(sys.argv[1])

    try:
        hentai.loadData()
    except ConnectionErrorNHentai as e:
        print(e)
        return
    hentai.analyzeData()
    hentai.downloadHentai()
    print("###############")
    print("# Hentai Info #")
    print("###############")
    print(hentai)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Write a code")
    else:
        downloadHentai(sys.argv[1])
