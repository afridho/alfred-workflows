#!/usr/bin/python
# encoding: utf-8
#
# Copyright (c) 2022 Ridho Zega
#
# MIT License. See http://opensource.org/licenses/MIT
#
from __future__ import division, print_function, absolute_import
import json
import sys
import requests
from importlib import reload
requests.packages.urllib3.disable_warnings()
reload(sys)
import os
from utils import get_data

resi_number = os.environ['resi_number']
icon_name = os.environ['logo_icon'] if "logo_icon" in os.environ else 'icon.png'


def delivered(status):
    if status.lower() == "delivered":
        return (u'💯')
    else:
        return ''

def status_icon(status):
    switcher = {
        'PICKREQ': "🥡",
        'PICK' : '🛻',
        'IN' : '🔼',
        'OUT': '🔽',
        'ANT' : '🛵',
        'UNPICK' : '🗃️',
        'CANCEL' : '😥',
        'DELIVERED' : ''
    }
    status_icon = switcher.get(status, status)
    return (f"{status} {status_icon}")
    
def data_dummy():
    fileJson = f"response_dummy.json"
    f = open(fileJson)
    resi_saved = json.load(f)
    return resi_saved

def details(query=None):
    data_options = get_data.from_file(resi_number)
    # data_options = data_dummy()
    # data_options = []
    
    data_result = data_options['sicepat']['result']['track_history']
    posts = sorted(data_result, key=lambda k: k['date_time'], reverse=True)
    
    # variables
    result = []
    
    if 'new_resi' in os.environ and posts[0]['status'] != "DELIVERED":
        result.append({
                    'title':f"{'Add resi number » type your product name to save ☑︎' if len(query) == 0 else ('save ' +  query + '✅')}",
                    'subtitle': f"No resi: {resi_number}",
                    'valid': False if len(query) == 0 else True,
                    'arg' : 'save',
                    'icon': {
                        'path' : 'icons/add_icon.png'
                    },
                    'variables' : {
                                'resi_number' :  resi_number,
                                'product_name' : query
                            },
                    })
        if len(query) > 0 and query != resi_number:
            posts = []
    
    for post in posts:
        result.append({
                    'title':f"{(post['city'] if 'city' in post else post['receiver_name']) + delivered(post['status'])}",
                    'subtitle': f"{status_icon(post['status'])}   ||   {post['date_time']}",
                    'valid':True,
                    'icon' : {
                        'path' : f"{icon_name}",
                    },
                    'text' : {
                        'largetype' : f"{(post['city'] if 'city' in post else post['receiver_name']) + delivered(post['status'])}",
                    },
                    'mods' : {
                        'cmd' : {
                            'subtitle':f"{(post['city'] if 'city' in post else post['receiver_name']) + delivered(post['status'])}",
                        }
                    }
                    })
    if len(query) == 0 or query == resi_number:
        result.append({
                        'title':'Back',
                        'subtitle':'',
                        'icon': {
                            'path' : 'icons/back.png',
                        },
                        'arg' : 'back',
                        'valid':True
            
                        })
                    
            
    return result

def main():
    SEARCH = sys.argv[1] if len(sys.argv) >= 2 else None
    posts  = details(query=SEARCH)
    data = json.dumps({"items": posts }, indent=4)
    print(data)

if __name__ == '__main__':
    main()
    # get_data_options()
    # settings()
