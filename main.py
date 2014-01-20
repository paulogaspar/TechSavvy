from bottle import route, run, template, static_file, request
import facebook
import json
from datetime import datetime
import PyRSS2Gen
import os
import urllib2
import re


# Obtain access token
access_token = ""
try:
	with open("access_token.txt") as f:
		access_token = f.readlines()[0]
except:
	access_token = os.environ.get("FB_KEY")


# TechSavvy group ID
ts_group_id = "289057704456073" 


# Get feed as python dictionary
def get_feed_dict():

	# Get group feed
	graph = facebook.GraphAPI(access_token)
	ts_group_feed = graph.get_connections(ts_group_id, "feed")

	return ts_group_feed


# Get techsavvy feed content in json
@route('/content/json')
def content_json():

	# Get group feed
	ts_group_feed = get_feed_dict()

	return json.dumps(ts_group_feed["data"])	


# Get techsavvy feed content in json
@route('/content/rss')
def content_rss():

	# Get group feed
	ts_group_feed = get_feed_dict()
	item_list = []
	for post in ts_group_feed["data"]:
		url = "https://www.facebook.com/groups/tech.savvyness/permalink/%s/" % (post.get("id").split('_')[1])
		rssitem = PyRSS2Gen.RSSItem(
		title = post.get("name", "Title"),
		link = url,
		description = post.get("message", ""),
		guid = PyRSS2Gen.Guid(url),
		pubDate = datetime.strptime(post.get('updated_time')[:-5],'%Y-%m-%dT%H:%M:%S'))
		item_list.append(rssitem)
    
	rss = PyRSS2Gen.RSS2(
    title = "TechSavvy RSS feed",
    link = "https://www.facebook.com/groups/tech.savvyness/",
    description = "The latest news by Tech Savvies",
    lastBuildDate = datetime.now(),
    items = item_list)

	return rss.to_xml()


# Serve static files
@route('/static/<filename:path>')
def server_static(filename):
    return static_file(filename, root='./')


# Fetch one image from url. Returns the image url.
@route('/api/fetchImage')
def fetch_image():
	url = request.query.url
	if url is None or url == '':
		return ''
	html = None
	try:
		response = urllib2.urlopen(url)
		html = response.read()
		p = re.compile('<meta[^>]+og:image[^>]+>', re.IGNORECASE)
		meta = p.search(html).group()
		if meta is None:
			return ''
		p = re.compile('content="[^"]+"', re.IGNORECASE)
		imageurl = p.search(meta).group()
		if imageurl is None:
			return ''
		else:
			return imageurl[9:-1]
	except:
		try:
			p = re.compile(r'("|\'|\()[^"]+(.jpg|.png|.gif)("|\'|\))', re.IGNORECASE)
			imageurl = p.search(html).group()
			if imageurl is None:
				return ''
			else:
				imageurl = imageurl[1:-1]
				if imageurl.startswith('//') or imageurl.startswith('http'):
					return imageurl
				elif imageurl[0]=='/':
					return url[0 : url.find('/',8)]+imageurl
				else:
					if url.endswith('/'):
						return url+imageurl
					else:
						return url+'/'+imageurl
		except Exception as e:
			print e
			return ''


# Fetch description from metadata. Returns the description.
@route('/api/fetchDescription')
def fetch_description():
	url = request.query.url
	if url is None or url == '':
		return ''
	html = None
	try:
		response = urllib2.urlopen(url)
		html = response.read()
		p = re.compile('<meta[^>]+og:description[^>]+>', re.IGNORECASE)
		meta = p.search(html).group()
		if meta is None:
			return ''
		p = re.compile('content="[^"]+"', re.IGNORECASE)
		description = p.search(meta).group()
		if description is None:
			return ''
		else:
			return description[9:-1]
	except:
		return ''


# Main access point. Returns main.html
@route('/')
def index():

	return template('main.html')


# Run bottle server
if __name__ == '__main__':
	run(host='0.0.0.0', port=os.environ.get("PORT", 8080), reloader=True)