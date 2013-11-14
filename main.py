from bottle import route, run, template
import facebook
import json


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

	return ""


# Testing with a bogus index page. In the future this 
# should only return the html file to the client.
@route('/')
def index():

	# Get group feed
	ts_group_feed = get_feed_dict()
	
	# Create output
	output = ""
	for post in ts_group_feed["data"]:
		author_name = unicode(post["from"]["name"])
		author_message = unicode(post["message"]) if "message" in post else ""
		
		post_picture = unicode(post["picture"]) if "picture" in post else ""
		post_name = unicode(post["name"]) if "name" in post else ""
		post_description = unicode(post["description"]) if "description" in post else ""

		post_block = "<b>"+author_name+"</b><img src='"+post_picture+"'/><i>"+post_name+"</i><h3>"+author_message+"</h3>"

		output = output + post_block + "<br/>"

	return output


# Run bottle server
if __name__ == '__main__':
	run(host='localhost', port=8080)