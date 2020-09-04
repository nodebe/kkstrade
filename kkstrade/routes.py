import flask
from flask import render_template, url_for, flash, redirect, request
# from kkstrade import app
from flask import Flask
from kkstrade.webscrape import get_data

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
	search = request.args.get('search')
	data=''
	if search != None and search != '' and search != ' ':
		data = get_data(search)
	return render_template('index.html', data=data)