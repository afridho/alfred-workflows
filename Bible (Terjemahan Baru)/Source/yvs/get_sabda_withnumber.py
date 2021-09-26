import requests
from bs4 import BeautifulSoup
import sys
import re

query = sys.argv[1]


url = 'https://alkitab.sabda.org/api/passage.php?passage='+query

document = requests.get(url)

soup= BeautifulSoup(document.content,"lxml-xml")

def title():
        source = soup.select_one("title").text
        title = source+" (TB)"
        print(title)


def content():
        total = []
        for el in soup.find_all(["number", "text"]):  
                total.append(el.text)
        bible = ''.join(total)
        r = re.compile(r'(\s*)((?:\s*\d)+)', re.I)
        compile = r.sub(r'\1[\2] ', bible).replace(';', '; ')
        if (len(total)) > 2:
                print(compile.replace('[', '\n['))
        else:
                print("")
                print(compile)

title()
content()

