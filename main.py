#curl -I -H 'If-None-Match: "225e025cd3a5f36d6dc2c42ace4b2734"'  -s -H "Authorization: token $GITHUB_API_KEY" https://api.github.com/repos/kubernetes/kubernetes/events?page=5
import os
import sys
import time

import requests

GH_API_KEY = os.environ.get('GITHUB_API_KEY')
ttvopenfeed_host = "localhost:3000"

if GH_API_KEY is None:
    print("Please set the GITHUB_API_KEY env variable")
    sys.exit(1)

#slug = 'nibalizer/dotfiles'
slug = 'kubernetes/kubernetes'
etag = ""

headers = {
        'user-agent': 'ttv-opensourcefeed/0.0.1',
        'If-None-Match': etag,
        'Authorization': "token " + GH_API_KEY,
        }
url = "https://api.github.com/repos/" + slug + "/events"

print("getting events for ", slug)
r = requests.get(url, headers=headers)
print(r.status_code)
print("Length: ", len(r.json()))
print(r.headers['ETag'])
print(r.headers['X-Poll-Interval'])
print(r.headers['X-RateLimit-Remaining'])
#curl -I -H 'If-None-Match: "225e025cd3a5f36d6dc2c42ace4b2734"'  -s -H "Authorization: token $GITHUB_API_KEY" https://api.github.com/repos/kubernetes/kubernetes/events?page=5

"""

if 'W' in r.headers['ETag']:
    etag = r.headers['ETag'][2:] # there is a leading "W/", signifies a 'weak etag'
else:
    etag = r.headers['ETag']
#from pdb import set_trace; set_trace()

time.sleep(1)

headers = {
        'user-agent': 'ttv-opensourcefeed/0.0.1',
        'If-None-Match': etag,
        'Authorization': "token " + GH_API_KEY,
        }
url = "https://api.github.com/repos/" + slug + "/events"

print("getting events for ", slug)
r = requests.get(url, headers=headers)
print(r.status_code)
if r.status_code == 200:
    print("Length: ", len(r.json()))
    print(r.headers['X-Poll-Interval'])
print(r.headers['ETag'])
print(r.headers['X-RateLimit-Remaining'])
"""


def process_github_event(ev):
    repo_name = ev['repo']['name']
    user_name = ev['actor']['login']
    event_type = ev['type']
    str_rep = "User: {0} did a {1} on {2}".format(user_name, event_type, repo_name)
    return str_rep



events =  r.json()
#print(events[0])

for ev in events:
    ev_str = process_github_event(ev)
    print(ev_str)
    requests.post("http://" + ttvopenfeed_host + "/submit", json={"message": ev_str})
