from bottle import route, run, template
import facebook
import json
import pprint

# Obtain access token
access_token = ""
with open("access_token.txt") as f:
	access_token = f.readlines()[0]

# TechSavvy group ID
ts_group_id = "289057704456073" 


# Get techsavvy feed content in json
@route('/getcontent')
def content():

	# Get group feed
	graph = facebook.GraphAPI(access_token)
	ts_group_feed = graph.get_connections(ts_group_id, "feed")

	return json.dumps(ts_group_feed["data"])	


# Testing with a bogus index page. In the future this 
# should only return the html file to the client.
@route('/')
def index():

	# Get group feed
	graph = facebook.GraphAPI(access_token)
	ts_group_feed = graph.get_connections(ts_group_id, "feed")
	
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


run(host='localhost', port=8080)