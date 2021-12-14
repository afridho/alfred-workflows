# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from workflow import Workflow
from collections import OrderedDict



def get_data(query):
    url = 'http://kateglo.com/index.php?op=1&phrase='+ query +'&lex=&type=&src=&mod=dictionary&srch=Cari'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    
    keys, values = [], []
    for dl in soup.findAll("dl"):
        for dt in dl.findAll("dt"):
            keys.append(dt.text.strip())
        for dd in dl.findAll("dd"):
            values.append(dd.text.strip()[2:])
    x = (dict(zip(keys, values)))
    return OrderedDict(sorted(x.items(), key=lambda t: t[0])) # change (sort) order Dict to normal return
    
def large_text(kata, arti):
    """Prettier Large Text to text indent""" 
    if len(arti) < 35:
        return ('// '+ kata + ' //'+'\n'+ arti +'.')
    else:
        return ('// '+ kata + ' //'+'\n\n'+ arti +'.')
    
def copy_text(arti):
    return "(" + arti + ")"

def clean_words(arti):
   return arti.replace("(Dok) ", "").replace("(ki) ", "").replace("(Adm) ", "").replace("(ark) ", "").replace("(Min) ", "").replace("(Tern) ", "")[:-1]

def main(wf):
    if len(wf.args):
     query = wf.args[0]
    else:
     query = None
     
    posts = get_data(query)
    if posts:
        for kata, arti in posts.items():
            wf.add_item(
                    title=kata.capitalize(),
                    subtitle=str(clean_words(arti)),
                    largetext=large_text(kata,str(clean_words(arti))),
                    copytext=copy_text(str(clean_words(arti))),
                    quicklookurl= 'http://kateglo.com/?mod=dictionary&action=view&phrase=' + kata,
                    valid='True',
                    arg=str(clean_words(arti))
                    )
    else:
            wf.add_item(
                title="Kata Tidak Ditemukan", icon='not_found.png', valid='True', arg='null'
            )

    # Send the results to Alfred as XML
    wf.send_feedback()
 
if __name__ == u"__main__":
 wf = Workflow()
 sys.exit(wf.run(main))
