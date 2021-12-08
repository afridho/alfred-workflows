import requests
from bs4 import BeautifulSoup
import sys

query = sys.argv[1]


url = 'https://alkitab.sabda.org/api/passage.php?passage='+query

document = requests.get(url)

soup= BeautifulSoup(document.content,"lxml-xml")

def content():
        total=[]
        
        for el in soup.find_all("text"):
                total.append(el.text)
        bible = ' '.join(total)
        print(bible)
content()


