# from hypothesis_settings import USERNAME, PASSWORD
import requests
import json
from itertools import islice
from urllib import urlencode
import run_naive

# To sign up for a username go to http://hypothes.is/alpha and download the Chrome Extension
# Use those details to access the API. 
USERNAME = raw_input("Enter username:")
PASSWORD = raw_input("Enter password:")


# do get to get 2 tokens CSFR
# https://www.owasp.org/index.php/Cross-Site_Request_Forgery_(CSRF)_Prevention_Cheat_Sheet
# http://list.hypothes.is/archive/dev/2013-10/0000096.html
# GET request /app and take the value of the beaker.session.id and XSRF-TOKEN Set-Cookie headers. 
# Pass these both back in the POST request in the Cookie header.

# http://www.python-requests.org/en/v1.1.0/user/quickstart/#cookies


### Customize what the area to evaluate is.
### Print comment and then rating.
# USER = raw_input("Enter a username to evaluate:")
# URL
# TAG
# GROUP

### Defaults: 
USERS = ["JakeHartnell", "dwhly", "tilgovi", "pbrantley", "futureofthebook"]

url = "https://hypothes.is/app"
r = requests.get(url)
cookies = r.cookies

payload = {"username":USERNAME,"password":PASSWORD}

data = json.dumps(payload)
headers = {'content-type':'application/json;charset=UTF-8'}

r = requests.post(url="https://hypothes.is/app?__formid__=login", data=data, cookies=cookies, headers=headers)
ResponseDict = json.loads(r.text)

if ResponseDict['flash'].get('success') == ['You are now logged in.']:
    token = ResponseDict['model']['token']
else:
    token = None

def search(user, offset=0):
    
    headers = {"X-Annotator-Auth-Token": token}
    page_size = 10
    user_acct = "acct:{user}@hypothes.is".format(user=user)
    
    limit=page_size
    
    more_results = True

    while more_results:
        search_dict = {'user':user_acct, 'limit':limit, 'offset':offset}
        url = "https://api.hypothes.is/search?{query}".format(query=urlencode(search_dict))
        
        r = requests.get(url, headers=headers)
        ResponseDict = json.loads(r.text)
        rows = ResponseDict.get("rows")
        
        if len(rows):
            for row in rows:
                yield row
            offset += page_size
        else:
            more_results = False

for user in USERS:
    for (i,row) in enumerate(search(user=user, offset=0)):
        if 'text' in row.keys():
            comment = row['text']
            score = run_naive.classify_with_NB(comment)
            print i, comment, score

