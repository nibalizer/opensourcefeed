import os
import sys
import time

import requests

GH_API_KEY = os.environ.get('GITHUB_API_KEY')
ttvopenfeed_host = "localhost:3000"
slug = 'kubernetes/kubernetes'
etag = ""
sleep_cycle = 60

seen_events = {}

if GH_API_KEY is None:
    print("Please set the GITHUB_API_KEY env variable")
    sys.exit(1)

def process_event_data(ev):
    repo_name = ev['repo']['name']
    user_name = ev['actor']['login']
    event_type = ev['type']
    date = ev['created_at']
    event_id = ev['id']
    seen_events[event_id] = True
    str_rep = "User: {0} did a {1} on {2} at {3}".format(
            user_name,
            event_type,
            repo_name,
            date)
    return str_rep

def process_events(events):
    for ev in events:
        if seen_events.get(ev['id']) is None:
            ev_str = process_event_data(ev)
            print(ev_str)
            requests.post("http://" + ttvopenfeed_host + "/submit", json={"message": ev_str})

def get_events(slug, etag):
    headers = {
            'user-agent': 'ttv-opensourcefeed/0.0.1',
            'If-None-Match': etag,
            'Authorization': "token " + GH_API_KEY,
            }
    url = "https://api.github.com/repos/" + slug + "/events"
    print("getting events for ", slug)
    r = requests.get(url, headers=headers)
    print("Status Code: ", r.status_code)
    print("Rate limit remaining:" , r.headers['X-RateLimit-Remaining'])
    if r.status_code == 200:
        process_events(r.json())
        #print(r.headers['ETag'])
        print(r.headers['X-Poll-Interval'])
    else:
        print("No new data")
    if 'W' in r.headers['ETag']:
        etag = r.headers['ETag'][2:] # there is a leading "W/", signifies a 'weak etag'
    else:
        etag = r.headers['ETag']
    return etag

while True:
    print("ETag: ", etag)
    etag = get_events(slug, etag)
    time.sleep(60)
