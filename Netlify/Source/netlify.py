# -*- coding: utf-8 -*-

import sys
import requests
import json
import datetime
import os
import datetime as dt
from workflow import Workflow

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
CACHE_TIME = os.getenv('CACHE_TIME') * 3600

def get_recent_projects():
 url = 'https://api.netlify.com/api/v1/sites'
 headers = {
  'Authorization': "Bearer "+ACCESS_TOKEN,
 }
 response = requests.request("GET", url, headers=headers)
 posts = response.json()
 return posts

def search_key_for_post(post):
 """Generate a string search key for a post"""
 elements = []
 elements.append(post['name'])  # title of post
 # elements.append(post['custom_domain'])  # post tags
 # elements.append(post['extended'])  # description
 return u' '.join(elements) 

def get_time(time):
 g = datetime.datetime.strptime(time,"%Y-%m-%dT%H:%M:%S.%fZ") + dt.timedelta(hours=7)
 c = g.strftime("%d-%m-%Y %H:%M")
 return (c)

def get_status_build(status):
 if status == 'True':
    return u'\U0001F6B8'
 else:
    return("")


def main(wf):

 # Get query from Alfred
 if len(wf.args):
     query = wf.args[0]
 else:
     query = None

 posts = wf.cached_data('posts', get_recent_projects, max_age=CACHE_TIME)
   
 # posts = get_recent_projects()

 if query:
        posts = wf.filter(query, posts, key=search_key_for_post, min_score=20)


 for post in posts:
     wf.add_item(
                 title=post['name']+' '+get_status_build(str(post['build_settings']['stop_builds'])),
                 subtitle=(post['custom_domain'] or post['default_domain']) +' '+(u'\u27A4')+ ' Last build '+get_time(post['updated_at']),
                 icon='icon.png',
                 arg=post['admin_url']+','+post['deploy_id']+','+post['url']+','+post['build_settings']['repo_url']+','+post['account_name']+','+post['site_id']+','+str(post['build_settings']['stop_builds'])+','+post['name'],
                 quicklookurl= post['screenshot_url'],
                 valid='True',
                 )

 # Send the results to Alfred as XML
 wf.send_feedback()


if __name__ == u"__main__":
 wf = Workflow()
 sys.exit(wf.run(main))