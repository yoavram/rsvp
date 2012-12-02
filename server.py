# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, jsonify, send_file
import os

# add environment variables using 'heroku config:add VARIABLE_NAME=variable_name'
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
FILENAME = "names.txt"

app = Flask(__name__)
app.config.from_object(__name__)  
if app.debug:
	print " * Running in debug mode"

def add_name(name):
	f = open(FILENAME,'a')
	f.write(name.encode('utf-8'))
	f.write('\n')
	f.close()

def get_names():
	f = open(FILENAME)
	names = f.readlines()
	f.close()
	names = [n.decode('utf-8') for n in names]
	return names

@app.route("/",  methods=['GET', 'POST'])
def index():
	names = get_names()
	if request.method == 'GET':
		return render_template("index.html", total=len(names))
	else:
		name = request.form['name']
		if name in [u'שם הסטודנט', u'', '', u' ', ' '] :
			return render_template("index.html", total=len(names), error=u"נא מלא/י את השם בתיבת הטקסט")
		elif name == u'yoavram':
			return send_file(FILENAME)
		else:
			add_name(name)
			return render_template("index.html", name=name, total=len(names))


if __name__ == '__main__':
	# Bind to PORT if defined, otherwise default to 5000.
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port, debug=app.debug)
