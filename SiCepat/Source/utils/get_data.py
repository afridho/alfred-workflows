import requests
import json
import pathlib

baseUrl = "https://content-main-api-production.sicepat.com/public/check-awb/"
baseCache = 'Cache'
pathlib.Path('Cache').mkdir(parents=True, exist_ok=True) 

def web_url(no_resi=None): 
    url = f"{baseUrl}{no_resi}"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'} # use user-agent to prevent from blocked
    file_request = requests.get(url, headers=headers, verify=False)
    file = file_request.json()
    
    if 'sicepat' in file and file['sicepat']['status']['code'] == 200:
        with open((f"{baseCache}/{no_resi}.json"), 'w', encoding='utf-8') as f:
            json.dump(file, f, ensure_ascii=False, indent=4)   
    return file

def from_file(no_resi=None):
    if pathlib.Path(f"{baseCache}/{no_resi}.json").is_file():
        fileJson = f"{baseCache}/{no_resi}.json"
        f = open(fileJson)
        resi_saved = json.load(f)
        return resi_saved
    else:
        web_url(no_resi)
    
    