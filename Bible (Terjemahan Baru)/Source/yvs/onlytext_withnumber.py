import requests
from bs4 import BeautifulSoup
import sys
import re

query = sys.argv[1]

url = 'https://alkitab.sabda.org/api/passage.php?passage='+query

document = requests.get(url)

soup= BeautifulSoup(document.content,"lxml-xml")

def content():
        total = []
        for el in soup.find_all(["number", "text"]):  
                total.append(el.text)
        bible = ''.join(total)
        r = re.compile(r'(\s*)((?:\s*\d)+)', re.I)
        compile = r.sub(r'\1[\2] ', bible).replace(';', '; ')
        # print(len(total))
        # print('total ',total)
        if (len(total)) > 2:
                proc = compile.replace('[', '\n[')
                print(proc.replace('\n', '', 1))
        else:
                print(compile)
           
content()


