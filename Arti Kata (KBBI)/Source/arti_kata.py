# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from workflow import Workflow
from collections import OrderedDict
import os

try:
    global_query = sys.argv[1] or ''
except:
    raise Exception('No query found')

def bool_convert(string_text):
    if string_text == "True" or string_text == "1" or string_text == "Yes":
        return True
    return False

# environment and variables
not_found_text = os.getenv('not_found_text') or "Kata Tidak Ditemukan"
suggestion_option = bool_convert(os.getenv('suggestion_option'))
baseUrl = os.getenv('base_Url')

def web_url(menu,query): #menu '1' for all words related, '3' for specific word
    url = '{}/index.php?op={}&phrase={}&lex=&type=&src=&mod=dictionary&srch=Cari'.format(baseUrl, menu,query)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'} # use user-agent to prevent from blocked
    page = requests.get(url, headers=headers, verify=False)
    return page.content

def get_data(menu, query):
    soup = BeautifulSoup(web_url(menu, query), "html.parser")
    
    keys, values = [], []
    for dl in soup.findAll("dl"):
        for dt in dl.findAll("dt"):
            keys.append(dt.text.strip())
        for dd in dl.findAll("dd"):
            values.append(dd.text.strip()[2:])
    if menu == 3: # if else for save load time
        return dict(zip(keys, values))
    elif menu == 1:
        x = dict(zip(keys, values))
        return OrderedDict(sorted(x.items(), key=lambda x: x[0])) # change (sort) order Dict to normal return
    else:
        return 'error'
    
def large_text(kata, arti):
    """Prettier Large Text to text indent""" 
    if len(arti) < 35:
        return ('// '+ kata + ' //'+'\n'+ arti +'.')
    else:
        return ('// '+ kata + ' //'+'\n\n'+ arti +'.')
    
def copy_text(arti):
    return "(" + arti + ")"
    
def clean_words(arti_source):
    arti = str(arti_source)
    if arti[:2] == "j ":
        return arti.replace("j ", "")
    elif arti[:6] == "(Olr) ":
        return arti.replace("(Olr) ", "")
    elif arti[:5] == "(Ar) ":
        return arti.replace("(Ar) ", "")
    elif arti[:6] == "(Ark) ":
        return arti.replace("(Ark) ", "")
    elif arti[:5] == "(Jw) ":
        return arti.replace("(Jw) ", "")
    elif arti[:6] == "(Sas) ":
        return arti.replace("(Sas) ", "")
    else:
        return arti.replace("(Dok) ", "").replace("(ki) ", "").replace("(Adm) ", "").replace("(ark) ", "").replace("(Min) ", "").replace("(Tern) ", "")[:-1]

def main(wf):
    ql_link = '{}/?mod=dictionary&action=view&phrase='.format(baseUrl)

    if len(wf.args) == 1:
     query = wf.args[0]
     posts = get_data(3, query)
    elif len(wf.args) == 2:
     query = wf.args[1] 
     posts = get_data(1, query)
    else:
     query = None
     
     
    if suggestion_option: 
        if posts:
            for kata, arti in posts.items():
                wf.add_item(
                        title=kata.capitalize(),
                        subtitle=clean_words(arti),
                        largetext=large_text(kata,clean_words(arti)),
                        copytext=copy_text(clean_words(arti)),
                        quicklookurl= '{}{}'.format(ql_link, kata),
                        valid='True',
                        modifier_subtitles={'alt': 'Temukan kata yang berkaitan'},
                        arg=kata
                        )
                
                
        else:
            # query = wf.args[1] 
            posts = get_data(1, global_query)
            if posts:
                for kata, arti in posts.items():
                    wf.add_item(
                        title=kata.capitalize(),
                        autocomplete=kata.capitalize(),
                        subtitle=clean_words(arti),
                        largetext=large_text(kata,clean_words(arti)),
                        copytext=copy_text(clean_words(arti)),
                        quicklookurl= '{}{}'.format(ql_link, kata),
                        valid='True',
                        modifier_subtitles={'alt': 'Temukan kata yang berkaitan'},
                        arg=kata
                        )
            else:
                wf.add_item(
                    title=not_found_text, icon='none', valid='True', arg=query, modifier_subtitles={'cmd': 'Cari disemua kata berkaitan'},
                )

        
    else:
        if posts:
            for kata, arti in posts.items():
                wf.add_item(
                        title=kata.capitalize(),
                        subtitle=clean_words(arti),
                        largetext=large_text(kata,clean_words(arti)),
                        copytext=copy_text(clean_words(arti)),
                        quicklookurl= '{}{}'.format(ql_link, kata),
                        valid='True',
                        modifier_subtitles={'alt': 'Temukan kata yang berkaitan'},
                        arg=kata
                        )
        else:
            wf.add_item(
                title=not_found_text, icon='none', valid='True', arg=query, modifier_subtitles={'cmd': 'Cari disemua kata berkaitan'},
                )
    # Send the results to Alfred as XML
    wf.send_feedback()
 
if __name__ == u"__main__":
 wf = Workflow()
 sys.exit(wf.run(main))