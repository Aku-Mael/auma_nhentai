from bs4 import BeautifulSoup
import requests
import sys


HENTAI_PAGE = "https://nhentai.net/g/"
COVER_PAGE = "https://t.nhentai.net/galleries/"


class Hentai():

    def __init__(self, code):
        # Id where the files are located
        self.id = None

        # Properties to download
        self.code = code
        self.title = None
        self.pages = None
        self.parodies = []
        self.characters = []
        self.tags = []
        self.artists = []
        self.groups = []
        self.languages = []
        self.categories = []

        # A BeautifulSoup object on the page
        self.data = None

    # Download html required to extract the data
    def loadData(self):
        link = HENTAI_PAGE + self.code + "/"
        html = requests.get(link)
        self.data = BeautifulSoup(html.text, "lxml")
        
    # Analyze the html to get the data
    def analyzeData(self):
        if not self.data:
            return False
        
        self.title = self.data.title.string.replace(' » nhentai: hentai doujinshi and manga', '')
        tags = self.data.find(id='tags')

        for tag in tags.find_all('div'):
            for item in tag.select('.name'):
                if tag.get_text().find('Parodies') > 0:
                    self.parodies.append(item.get_text())
                elif tag.get_text().find('Characters') > 0:
                    self.characters.append(item.get_text())
                elif tag.get_text().find('Tags') > 0:
                    self.tags.append(item.get_text())                
                elif tag.get_text().find('Artists') > 0:
                    self.artists.append(item.get_text())                    
                elif tag.get_text().find('Groups') > 0:
                    self.groups.append(item.get_text())
                elif tag.get_text().find('Languages') > 0:
                    self.languages.append(item.get_text()) 
                elif tag.get_text().find('Categories') > 0:
                    self.categories.append(item.get_text())
                elif tag.get_text().find('Pages') > 0:
                    self.pages = item.get_text()
                    
        url = self.data.find(id='cover').find_all('img')[-1].get('src')
        self.id = url.replace(COVER_PAGE, '').replace('/cover.', '').replace('jpg', '').replace('png', '')
    
    
    def __str__(self):
        string = ""
        
        string = "Code: " + self.code
        
        if self.id:
            string = string + "\nID: " + str(self.id)
        if self.title :
            string = string + "\nTitle: " + self.title
        if self.pages:
            string = string + "\nPages: " + str(self.pages)
        if self.parodies:
            string = string + "\nParodies: " + str(self.parodies)
        if self.characters:
            string = string + "\nCharacters: " + str(self.characters)
        if self.tags:
            string = string + "\nTags: " + str(self.tags)
        if self.artists:
            string = string + "\nArtists: " + str(self.artists)
        if self.groups:
            string = string + "\nGroups: " + str(self.groups)
        if self.languages:
            string = string + "\nLanguages: " + str(self.languages)
        if self.categories:
            string = string + "\nCategories: " + str(self.categories)
        
        return string


def loadHentai(code):
    try:
        int(code)
    except:
        print("Write a code")
        return
        
    hentai = Hentai(code)
    hentai.loadData()
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
