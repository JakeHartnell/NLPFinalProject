from pprint import pprint
import requests
import json

import datetime
import time

from xml.dom.minidom import parseString

import gdata.youtube
import gdata.youtube.service

redditComments = []
output_dir = "/Users/dirkdewit/Documents/School/Master HTI/Internationaal Semester/Applied Natural Language Processing/Final Assignment/NLPFinalProject/data/heldout/"

def redditData(url, tag):
	r = requests.get(url)
	data = json.loads(r.text)

	article = data[0]['data']['children'][0]
	comments = data[1]['data']['children']

	for child in comments:
		#print child['data']['id'], child['data']['author'], "\r\n", child['data']['body']
		#print "Ups:", child['data']['ups'], "Downs:", child['data']['downs']
		comment = child['data']

		if 'body' in comment:
			comment = comment['body']

			if comment != "[deleted]":
				redditComments.append("##")
				redditComments.append(comment.encode('utf-8'))

			replies = child['data']['replies']

			if len(replies) > 0:
				getReplies(replies)

	print "Length: ", len(redditComments) / 2
	comments = '\n'.join(redditComments)
	writeToFile(tag, comments)

def getReplies(replies):
	replies = replies['data']['children']

	for reply in replies:
		comment = reply['data']
		if 'body' in comment:
			comment = comment['body']

			if comment != "[deleted]":
				redditComments.append("##")
				redditComments.append(comment.encode('utf-8'))

			newReplies = reply['data']['replies']

			if len(newReplies) > 0:
				getReplies(newReplies)

def youtubeData():
	for i in range(20000):

		maxResults = 10;
		j = i * maxResults

		if j == 0:
			j = 1

		print j
		print 

		r = requests.get(r'http://gdata.youtube.com/feeds/api/videos/kffacxfA7G4/comments?v=2&alt=json&key=AI39si6Y5zte7GQ73NJwVEuwtUVV2KgwfIOlSiRm1AdkE_2eJqo5vNZuYTTS-_g-NGKly4T8pO-LEgLuTZ3bswHfaaMGAJm0pw&max-results=10&start-index=%s' % j)
		data = json.loads(r.text)

		comments = data['feed']['entry']
	
		for comment in comments:
			print comment['content']
			print

def youtubeDataAPI(key, tag):
	yt_service = gdata.youtube.service.YouTubeService()

	# Turn on HTTPS/SSL access.
	yt_service.ssl = True
	yt_service.developer_key = 'AIzaSyBdrBfWQJS4mptTMedD82Xy88LI13t_s7s'
	yt_service.client_id = 'NLTP'

	getAndPrintVideoCommentFeed(yt_service, key, tag)

def getAndPrintVideoCommentFeed(yt_service, video_id, tag):
	feed = yt_service.GetYouTubeVideoCommentFeed(video_id=video_id)

	i = 0
	commentsList = []

	while feed is not None:
		for comment in feed.entry:
			#print i, comment
			i = i + 1

			dom = parseString(comment.ToString())
			entry = dom.getElementsByTagName('ns0:entry')

			for node in entry:
				child = node.getElementsByTagName('ns0:content')[0].firstChild
				if child is not None:
					message = child.nodeValue
					commentsList.append('##')
					commentsList.append(message.encode('utf-8'))

		if i < 600:
			next_link = feed.GetNextLink()

			if next_link is None:
				feed = None
			else:
				feed = yt_service.GetYouTubeVideoCommentFeed(next_link.href)
		else:
			feed = None

	comments = '\n'.join(commentsList)
	writeToFile(tag, comments)

def writeToFile(file, comments):
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')
	g = open(output_dir + file + "_" + st + '.txt', "w")
	g.write(comments)
	g.close()

#redditData(r'http://www.reddit.com/r/AskHistorians/comments/1sj0ld/for_what_reasons_did_the_ancestors_of_the_inuit/.json', "good")
youtubeDataAPI("kffacxfA7G4", "bad")


