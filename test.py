from pprint import pprint
import requests
import json

r = requests.get(r'http://www.reddit.com/r/funny/comments/1pylzx/well_aint_that_a_bitch/.json')
data = json.loads(r.text)

article = data[0]['data']['children'][0]
comments = data[1]['data']['children']

for child in comments:
	print child['data']['id'], child['data']['author'], "\r\n", child['data']['body']
	print "Ups:", child['data']['ups'], "Downs:", child['data']['downs']
	print