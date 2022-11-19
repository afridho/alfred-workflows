import requests
import json
import os
import sys

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')

url = "https://api.netlify.com/api/v1/sites/"+sys.argv[2]

def toggle(build_status):
  if build_status == "True":
    return False
  else:
    return True

payload = json.dumps({
  
  "build_settings": {
    "stop_builds": toggle(sys.argv[1])
  }
})
headers = {
  'Content-Type': 'application/json',
  'Authorization': "Bearer "+ACCESS_TOKEN,
}

response = requests.request("PATCH", url, headers=headers, data=payload)

if response.status_code == 200:
  print('success')
else:
  print('fail')
