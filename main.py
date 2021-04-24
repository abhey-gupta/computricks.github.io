from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import json

with open('config.json', 'r') as json_file:
    params = json.load(json_file)['params']

app = Flask(__name__)

local_server = True
if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']
db = SQLAlchemy(app)

class Contacts(db.Model):
    # sno, fname, lname, email, message, date
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    message = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact', methods = ['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Add entry to the database
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        entry = Contacts(name=name, email=email, message=message)

        db.session.add(entry)
        db.session.commit()

    return render_template('contact.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/search')
def search():
    return render_template('search.html')

app.run(debug=True)