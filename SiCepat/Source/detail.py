# -*- coding: utf-8 -*-

import sys
import requests
import json
import datetime
import os
import datetime as dt
from workflow import Workflow


def get_recent_projects(resi):
    url = 'https://content-main-api-production.sicepat.com/public/check-awb/'+resi
    response = requests.request("GET", url)
    posts = response.json()
    return posts

def delivered(status):
    if status == "ANT":
        return (u'🛵')
    else:
        return ''

def status(status):
    if status == "PICKREQ":
        return (status+' '+u'🥡')
    elif status =="PICK":
        return (status+' '+u'🛻')
    elif status =="IN":
        return (status+' '+u'🔼')
    elif status =="OUT":
        return (status+' '+u'🔽')
    else:
        return (status)

def main(wf):

 # Get query from Alfred
 if len(wf.args):
     query = wf.args[0]
 else:
     query = None
   
 result = get_recent_projects(query)

 if result['sicepat']['result']['last_status']['status'] == "DELIVERED":
    data_result = result['sicepat']['result']['track_history'][:-1]
 else:
    data_result = result['sicepat']['result']['track_history']
   
 posts = sorted(data_result, key=lambda k: k['date_time'], reverse=True)

 for post in posts:
    wf.add_item(
                 title=post['city']+' '+delivered(post['status']),
                 subtitle=status(post['status']) + '     |     '+post['date_time'],
                 largetext=post['city'],
                 valid='True',
                 )
 # Send the results to Alfred as XML
 wf.send_feedback()


if __name__ == u"__main__":
 wf = Workflow()
 sys.exit(wf.run(main))