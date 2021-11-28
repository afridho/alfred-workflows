# -*- coding: utf-8 -*-

import sys
import requests
import json
import os
from workflow import Workflow


def get_recent_projects(resi):
    url = 'https://content-main-api-production.sicepat.com/public/check-awb/'+resi
    response = requests.request("GET", url)
    posts = response.json()
    return posts

def main(wf):

 # Get query from Alfred
 if len(wf.args):
     query = wf.args[0]
 else:
     query = None
   
 post = get_recent_projects(query)

 
 if post['sicepat']['status']['code'] == 200 and post['sicepat']['result']['last_status']['status'] == "DELIVERED":
    wf.add_item(
                 title=post['sicepat']['result']['last_status']['receiver_name'],
                 subtitle=u'Delivered✅     |     '+post['sicepat']['result']['last_status']['date_time'],
                 arg=post['sicepat']['result']['waybill_number'],
                 quicklookurl= 'tes',
                 valid='True',
                 )
 elif post['sicepat']['status']['code'] == 200 and post['sicepat']['result']['last_status']['status'] != "DELIVERED":
    wf.add_item(
                 title=post['sicepat']['result']['last_status']['city'],
                 arg=post['sicepat']['result']['waybill_number'],
                 largetext=post['sicepat']['result']['last_status']['city'],
                 valid='True',
                 ),
    wf.add_item(
                 title=post['sicepat']['result']['last_status']['date_time'],
                 arg=post['sicepat']['result']['waybill_number'],
                 largetext=post['sicepat']['result']['last_status']['date_time'],
                 valid='True',
                 )
    wf.add_item(
                 title="sender: "+post['sicepat']['result']['sender'],
                 arg=post['sicepat']['result']['waybill_number'],
                 subtitle=post['sicepat']['result']['sender_address'],
                 largetext="sender: "+post['sicepat']['result']['sender'],
                 valid='True',
                 )
 elif post['sicepat']['status']['code'] == 400:
    wf.add_item(
                 title='Resi Number not found. Please check again.',
                 valid='True',
                 )
 else:
    wf.add_item(
                 title='Workflow error.',
                 valid='True',
                 )
 # Send the results to Alfred as XML
 wf.send_feedback()


if __name__ == u"__main__":
 wf = Workflow()
 sys.exit(wf.run(main))