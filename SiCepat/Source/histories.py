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
from utils import crud
requests.packages.urllib3.disable_warnings()
reload(sys)

def histories(search=None):
    data_options = crud.resi_saved()

    # variables
    result = []

    if len(data_options) > 0:
        for post in data_options:

            if search is not None and (post['no_resi'].lower().find(search.lower()) == -1) and (post['product_name'].lower().find(search.lower()) == -1):
                continue
            result.append({
                        'title':f"{post['product_name']}",
                        'subtitle':f"Last update: {post['last_update'] if post['last_update'] else 'None'} || Delivered: {'⛔️' if post['valid'] else '✅'}",
                        'arg': f"{post['no_resi']}",
                        'variables' : {
                            'resi_number' :  f"{post['no_resi']}",
                        },
                        'icon':{
                            'path' : f"icon.png"
                        },
                        'valid':True,
                        'mods' : {
                            'alt' : {
                                'subtitle' : f"{'Mark Finished (Delivered 🛵)' if post['valid'] else ''}",
                                'valid' : True,
                                'variables' : {
                                    'resi_number' :  f"{post['no_resi']}",
                                },
                            },
                            'ctrl' : {
                                'subtitle' : "Remove Resi Number",
                                'valid' : True,
                                'variables' : {
                                    'resi_number' :  f"{post['no_resi']}",
                                },
                            }
                        }
                        })
            
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


"""Run Script Filter."""
def main():
    SEARCH = sys.argv[1] if len(sys.argv) >= 2 else None
    posts  = histories(search=SEARCH)
    data = json.dumps({"rerun": 0.2, "items": posts }, indent=4) # make "rerun" : 0.2
    print(data)

if __name__ == '__main__':
    main()