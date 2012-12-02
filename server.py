# -*- coding: utf-8 -*-
from flask import Flask, request, render_template
import os
from os.path import exists

# add environment variables using 'heroku config:add VARIABLE_NAME=variable_name'
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
PASSWORD = u'yoavram'
FILENAME = "names.txt"

if not exists(FILENAME):
	open(FILENAME, 'w').close()

app = Flask(__name__)
app.config.from_object(__name__)  
if app.debug:
	print " * Running in debug mode"


def add_name(name):
	name = name.strip()
	f = open(FILENAME, 'a')
	f.write(name.encode('utf-8'))
	f.write('\n')
	f.close()


def get_names(file=False):
	f = open(FILENAME)
	if file:
		names = f.read()
		names = names.decode('utf-8')
	else:
		names = f.readlines()
		names = [n.decode('utf-8') for n in names if len(n.strip()) > 0]
	f.close()
	return names


def save_file(file_text):
	f = open(FILENAME, 'w')
	f.write(file_text.encode('utf-8'))
	f.close()


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
				file_text = get_names(True)
				return render_template("index.html", file_text=file_text, total=len(names))
			else:
				add_name(name)
				return render_template("index.html", name=name, total=len(names))
		elif 'file_text' in request.form:
			file_text = request.form['file_text']
			save_file(file_text)
			file_text = get_names(True)
			return render_template("index.html", file_text=file_text, total=len(names))


if __name__ == '__main__':
	# Bind to PORT if defined, otherwise default to 5000.
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port, debug=app.debug)
