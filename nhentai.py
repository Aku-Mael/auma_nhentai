from bs4 import BeautifulSoup
import requests
from requests.exceptions import ConnectionError
import sys


HENTAI_PAGE = "https://nhentai.net/g/"
COVER_PAGE = "https://t.nhentai.net/galleries/"


class Hentai():

    def __init__(self, code):
        # Id where the files are located
        self._id = None

        # Properties to download
        self._code = code
        self._title = None
        self._pages = None
        self._parodies = []
        self._characters = []
        self._tags = []
        self._artists = []
        self._groups = []
        self._languages = []
        self._categories = []

        # A BeautifulSoup object on the page
        self._data = None

    @property
    def id(self):
        return self.id

    @property
    def code(self):
        return self.code

    @property
    def title(self):
        return self.title
    
    @property
    def parodies(self):
        return self.parodies
    
    @property
    def characters(self):
        return self.characters

    @property
    def tags(self):
        return self.tags

    @property
    def artists(self):
        return self.artists

    @property
    def groups(self):
        return self.groups

    @property
    def languages(self):
        return self.languages

    @property
    def categories(self):
        return self.categories    
    
    # Download html required to extract the data
    def loadData(self):
        link = HENTAI_PAGE + self._code + "/"
        try:
            check = requests.get(link, timeout=1)
        except ConnectionError:
            raise ConnectionErrorNHentai("Connection failed")
            return
        except requests.Timeout:
            raise ConnectionErrorNHentai("Waiting time exceeded")
            return        
        
        if check.status_code == 404:
            raise ConnectionErrorNHentai("Error al buscar el código")
        else:
            self._data = BeautifulSoup(check.text, "lxml")
        
    # Analyze the html to get the data
    def analyzeData(self):
        if not self._data:
            return False
        
        self._title = self._data.title.string.replace(' » nhentai: hentai doujinshi and manga', '')
        tags = self._data.find(id='tags')

        for tag in tags.find_all('div'):
            for item in tag.select('.name'):
                if tag.get_text().find('Parodies') > 0:
                    self._parodies.append(item.get_text())
                elif tag.get_text().find('Characters') > 0:
                    self._characters.append(item.get_text())
                elif tag.get_text().find('Tags') > 0:
                    self._tags.append(item.get_text())                
                elif tag.get_text().find('Artists') > 0:
                    self._artists.append(item.get_text())                    
                elif tag.get_text().find('Groups') > 0:
                    self._groups.append(item.get_text())
                elif tag.get_text().find('Languages') > 0:
                    self._languages.append(item.get_text()) 
                elif tag.get_text().find('Categories') > 0:
                    self._categories.append(item.get_text())
                elif tag.get_text().find('Pages') > 0:
                    self._pages = item.get_text()
                    
        url = self._data.find(id='cover').find_all('img')[-1].get('src')
        self._id = url.replace(COVER_PAGE, '').replace('/cover.', '').replace('jpg', '').replace('png', '')
        return True
    
    
    def __str__(self):
        string = "Code: " + self._code
        
        if self._id:
            string = string + "\nID: " + str(self._id)
        if self._title :
            string = string + "\nTitle: " + self._title
        if self._pages:
            string = string + "\nPages: " + str(self._pages)
        if self._parodies:
            string = string + "\nParodies: " + str(self._parodies)
        if self._characters:
            string = string + "\nCharacters: " + str(self._characters)
        if self._tags:
            string = string + "\nTags: " + str(self._tags)
        if self._artists:
            string = string + "\nArtists: " + str(self._artists)
        if self._groups:
            string = string + "\nGroups: " + str(self._groups)
        if self._languages:
            string = string + "\nLanguages: " + str(self._languages)
        if self._categories:
            string = string + "\nCategories: " + str(self._categories)
        
        return string


class ConnectionErrorNHentai(Exception):
    """Error trying to establish a connection with nhentai"""
    def __init__(self, info="Undefined"):
        self.info = info
        super().__init__(self.info)




def loadHentai(code):
    try:
        int(code)
    except:
        print("Write a code")
        return
        
    hentai = Hentai(code)
    try:
        hentai.loadData()
    except ConnectionErrorNHentai as e:
        print(e)
        return
    hentai.analyzeData()
    print("###############")
    print("# Hentai Info #")
    print("###############")
    print(hentai)



if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Write a code")
    else:
        loadHentai(sys.argv[1])
