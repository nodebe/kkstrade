import flask
from flask import render_template, url_for, flash, redirect, request
from flask import Flask
from kkstrade.webscrape import get_data
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///searches.db'
db = SQLAlchemy(app)


@app.route('/')
@app.route('/index')
def index():
	search = request.args.get('search').strip(' ')
	search_test = ''.join(search.split())
	data=''
	if search_test.isalnum():
		data = get_data(search)
		search_data_input = Search(item=search,number=len(data),date=dt.now())
		db.session.add(search_data_input)
		db.session.commit()
	return render_template('index.html', data=data)

@app.route('/data')
def data():
	items = Search.query.all()
	return render_template('data.html', items=items)


'''
Database creation
'''
class Search(db.Model):
	id = db.Column(db.Integer, primary_key=True, unique=True)
	item = db.Column(db.String)
	number = db.Column(db.Integer)
	date = db.Column(db.DateTime)