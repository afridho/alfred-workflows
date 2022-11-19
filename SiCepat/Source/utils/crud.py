import json
from datetime import datetime
from pathlib import Path

fileName = './resi_saved.json'

# time variable
time_format = "%Y-%m-%d %H:%M"
parse_time_now = datetime.now()
time_now = parse_time_now.strftime(time_format)

def addData(no_resi=None, product_name=None):
    with open(fileName) as fp:
        listObj = json.load(fp)
        listObj.append({
            "no_resi": no_resi,
            "product_name": product_name,
            "valid" : True,
            "last_update" : ''
        })
    with open(fileName, 'w') as json_file:
        json.dump(listObj, json_file, 
                            indent=4,  
                            separators=(',',': '))
    print('Data saved.')
    
def deleteData(no_resi=None):
    with open(fileName, 'r') as f:
        my_list = json.load(f)
        for idx, obj in enumerate(my_list):
            if obj['no_resi'] == no_resi:
                my_list.pop(idx)
    with open(fileName, 'w') as f:
        f.write(json.dumps(my_list, indent=4))
"""End Delete Data Function"""

"""Begin Fill last_update if status delivered"""
def fillLastUpdate(no_resi=None, date=None):
    with open(fileName, 'r') as f:
        my_list = json.load(f)
        for idx, obj in enumerate(my_list):
            if obj['no_resi'] == no_resi:
                obj['last_update'] = date
    with open(fileName, 'w') as f:
        f.write(json.dumps(my_list, indent=4))

"""Begin Mark Finished Data"""
def markFinishedData(no_resi=None):
    with open(fileName, 'r') as f:
        my_list = json.load(f)
        for idx, obj in enumerate(my_list):
            if obj['no_resi'] == no_resi:
                obj['valid'] = False
    with open(fileName, 'w') as f:
        f.write(json.dumps(my_list, indent=4))

def resi_saved():
    path = Path(fileName)
    if path.is_file():
        fileJson = f"{fileName}"
        f = open(fileJson)
        resi_saved = json.load(f)
        return resi_saved
    else:
        """create empty json to prevent error"""
        with open(f"{fileName}", 'w') as f:
            json.dump([], f, indent=4)
        fileJson = f"{fileName}"
        f = open(fileJson)
        resi_saved = json.load(f)
        return resi_saved

# addData('50', 'debug')