# -*- coding: utf-8 -*-
from flask import Flask, request, render_template
from flask.ext.pymongo import PyMongo, ASCENDING 
import os
from datetime import datetime
import urllib
import urlparse 

DATE_FORMAT = "%d %B, %Y"

def db_name_from_uri(full_uri):
	ind = full_uri[::-1].find('/')
	return full_uri[-ind:]


def datetime_from_string(string):
	return datetime.strptime(string, DATE_FORMAT)


def string_from_datetime(datetime_obj):
	return datetime_obj.strftime(DATE_FORMAT)

### config params ########

# add environment variables using 'heroku config:add VARIABLE_NAME=variable_name'
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
MONGO_URI = os.environ.get('MONGOLAB_URI')
WEBSITE_URL = os.environ.get('WEBSITE_URL', 'http://localhost:5000/')

### init app ##########

app = Flask(__name__)
app.config.from_object(__name__)  
app.config.from_pyfile('config.py', True)
if app.debug:
	print " * Running in debug mode"

### init database ##########

app.config['MONGO_DBNAME'] = db_name_from_uri(app.config['MONGO_URI'])
mongo = PyMongo(app)
if mongo:
	print " * Connection to database established"
else:
	raise Exception("No Mongo Connection")

### template filters ######

app.jinja_env.filters['format_date'] = string_from_datetime


### helper functions #######

def process_form(form):
	date = form['date']
	if date:
		form['date'] = datetime_from_string(date)
	form['url'] = urlparse.urljoin(app.config["WEBSITE_URL"], 'event/' + urllib.quote_plus(form['event']))
	return form


def get_event(event):
	return mongo.db.events.find_one({"event":event})

def add_name(name, event):
	time = datetime.now()
	d = {'time':time, 'name':name}
	oid = mongo.db[event].insert(d)
	print "Added object to database:", oid


def get_names(event):
	cur = mongo.db[event].find(sort=[('time', ASCENDING)])
	names = [d['name'].strip() for d in cur]
	names = [n for n in names if len(n) > 0]
	return names


def save_editor(editor, event):
	mongo.db[event].drop()
	for n in editor.split('\n'):
		n = n.strip()
		add_name(n, event)


### handler functions #########

@app.route("/",  methods=['GET', 'POST'])
def create():
	if request.method == 'GET':
		return render_template("create.html")
	else:
		form = process_form(request.form.to_dict())
		oid = mongo.db.events.insert(form)
		print "Added object to database:", oid
		return render_template("create.html", form=form)


@app.route("/event/<string:event>",  methods=['GET', 'POST'])
def event(event):
	event = urllib.unquote_plus(event)
	event_details = get_event(event)
	names = get_names(event)
	if request.method == 'GET':
		return render_template("index.html", event=event, total=len(names))
	else:
		if 'name' in request.form:
			name = request.form['name']
			if name in [u'John Doe', u'', u'', u' ', u' ', u'Your Name...'] :
				return render_template("index.html", total=len(names), error=u"Please fill in your name")
			elif name == event_details['password']:
				editor = "\n".join(names)
				return render_template("editor.html", event=event, editor=editor, total=len(names))
			else:
				add_name(name, event)
				return render_template("index.html", event=event, name=name, total=len(names))
		elif 'editor' in request.form:
			editor = request.form['editor']
			save_editor(editor)
			file_text = "\n".join(names)
			return render_template("editor.html", event=event, editor=editor, total=len(names))

### MAIN ###########

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port, debug=app.debug)
