from __future__ import division, print_function, absolute_import
import json
import sys
from importlib import reload
reload(sys)
import sqlite3

databaseFile = 'kbbi.sqlite'
connection = sqlite3.connect(databaseFile)
cursor = connection.cursor()
    
def view_data(search_text=None):
    rows = cursor.execute(f"SELECT * FROM kamus WHERE lower(kata) = '{search_text}' limit 1").fetchall()
    if (len(rows) == 1):
        return rows
    else:
        return cursor.execute(f"SELECT * FROM kamus WHERE lower(kata) LIKE '%{search_text}%'").fetchall()

def save_text(search=None):
    data = view_data(search)  
    result = []
    if data:
        for i in data:
            result.append({
                'title': i[1].capitalize(),
                'subtitle' : i[2].replace('\n',' '),
                'valid' : True if len(data) <= 1 else False,
                'arg' : i[2],
                'autocomplete': i[1],
                'mods':{
                    'cmd' : {
                        'subtitle' : i[2].replace('\n',' ')
                    }
                },
                'text' : {
                    'largetype' : i[2] # no need to replace new line
                }
            })
    else:
        result.append({
            'title' : 'Kata Tidak Ditemukan',
            'valid' : False,
            'icon' : {
                'path' : 'not_found.png'
            },
            'mods' : {
                'cmd' : {
                    'subtitle' : ''
                }
            }
        })
    return result

    
def main():
    SEARCH = sys.argv[1] if len(sys.argv) >= 2 else None
    posts  = save_text(search=SEARCH)
    data = json.dumps({"rerun": 1,"items": posts }, indent=4) # "rerun":1,
    print(data)
