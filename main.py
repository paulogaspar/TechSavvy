from bottle import route, run, template, static_file
import facebook
import json
from datetime import datetime
import PyRSS2Gen
import os


# Obtain access token
access_token = ""
with open("access_token.txt") as f:
	access_token = f.readlines()[0]

# TechSavvy group ID
ts_group_id = "289057704456073" 


# Get feed as python dictionary
def get_feed_dict():

	# Get group feed
	graph = facebook.GraphAPI(access_token)
	ts_group_feed = graph.get_connections(ts_group_id, "feed")

	return ts_group_feed


# Get techsavvy feed content in json
@route('/getcontent/json')
def content_json():

	# Get group feed
	ts_group_feed = get_feed_dict()

	return json.dumps(ts_group_feed["data"])	


# Get techsavvy feed content in json
@route('/getcontent/rss')
def content_rss():

	# Get group feed
	ts_group_feed = get_feed_dict()
	item_list = []
	for post in ts_group_feed["data"]:
		url = "https://www.facebook.com/groups/tech.savvyness/permalink/%s/" % (post.get("id").split('_')[1])
		rssitem = PyRSS2Gen.RSSItem(
		title = post.get("name", "Title"),
		link = url,
		description = post.get("message", "").encode("utf-8"),
		guid = PyRSS2Gen.Guid(url),
		pubDate = datetime.strptime(post.get('updated_time')[:-5],'%Y-%m-%dT%H:%M:%S'))
		item_list.append(rssitem)
    
	rss = PyRSS2Gen.RSS2(
    title = "TechSavvy's RSS feed",
    link = "https://www.facebook.com/groups/tech.savvyness/",
    description = "The latest news on TechSavvy",
    lastBuildDate = datetime.now(),
    items = item_list)

	return rss.to_xml(encoding='utf-8')

# Serve static files
@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='./')


# Main access point. Returns main.html
@route('/')
def index():

	return template('main.html')


# Run bottle server
if __name__ == '__main__':
	run(host='localhost', port=os.environ.get("PORT",8080))