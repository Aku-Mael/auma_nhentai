# NHentai API
## Description
This is an API to interact with the web [NHentai] (https://nhentai.net) to know the information and download hentai through its code and using python3. It will show the following characteristics:
+ Name
+ Code
+ ID
- Parodies
- Characters
- Tags
- Artists
- Groups
- Languages
- Categories
- Pages
## Classes
### Hentai
This class stores the information corresponding to the manga associated with a code.
### DownloadHentai
This class contains a Hentai and a url where to download it.
## Use
**Consult information about a hentai**
python3 nhentai.py code
**Download a hentai**
python3 downloadNhentai.py [-u] [url] code
