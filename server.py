# -*- coding: utf-8 -*-
from flask import Flask, request, render_template
from flask.ext.pymongo import PyMongo, ASCENDING 
import os
from os.path import exists
from datetime import datetime

def db_name_from_uri(full_uri):
	ind = full_uri[::-1].find('/')
	return full_uri[-ind:]

# add environment variables using 'heroku config:add VARIABLE_NAME=variable_name'
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
MONGO_URI = os.environ.get('MONGOLAB_URI')
PASSWORD = u'yoavram'

app = Flask(__name__)
app.config.from_object(__name__)  
app.config.from_pyfile('config.py', True)
if app.debug:
	print " * Running in debug mode"

app.config['MONGO_DBNAME'] = db_name_from_uri(app.config['MONGO_URI'])
mongo = PyMongo(app)
if mongo:
	print " * Connection to database established"
else:
	raise Exception("No Mongo Connection")


def add_name(name):
	time = datetime.now()
	d = {'time':time, 'name':name}
	oid = mongo.db.general.insert(d)
	print "Added object to database:", oid


def get_names():
	cur = mongo.db.general.find(sort=[('time', ASCENDING)])
	names = [d['name'].strip() for d in cur]
	names = [n for n in names if len(n) > 0]
	return names


def save_file(file_text):
	mongo.db.general.drop()
	for n in file_text.split('\n'):
		n = n.strip()
		add_name(n)

@app.route("/",  methods=['GET', 'POST'])
def index():
	names = get_names()
	if request.method == 'GET':
		return render_template("index.html", total=len(names))
	else:
		if 'name' in request.form:
			name = request.form['name']
			if name in [u'שם הסטודנט', u'', '', u' ', ' '] :
				return render_template("index.html", total=len(names), error=u"נא מלא/י את השם בתיבת הטקסט")
			elif name == PASSWORD:
				file_text = "\n".join(names)
				return render_template("index.html", file_text=file_text, total=len(names))
			else:
				add_name(name)
				return render_template("index.html", name=name, total=len(names))
		elif 'file_text' in request.form:
			file_text = request.form['file_text']
			save_file(file_text)
			file_text = "\n".join(names)
			return render_template("index.html", file_text=file_text, total=len(names))


if __name__ == '__main__':
	# Bind to PORT if defined, otherwise default to 5000.
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port, debug=app.debug)
