
######################## Library #############################
from flask import Flask, flash, redirect, render_template, \
     request, url_for,Response, jsonify, send_from_directory
from flask import redirect,url_for,session,logging,request
import os
import csv
import time
import json
import jsonify
import requests
import warnings
import datetime
import numpy as np
import pandas as pd
import sqlite3 as sql
from flask import request
from flask import jsonify
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template
from werkzeug.utils import secure_filename
from werkzeug.utils import secure_filename

warnings.filterwarnings("ignore")

app = Flask(__name__)

UPLOAD_FOLDER = 'received_files'
ALLOWED_EXTENSIONS = ['png','jpg','jpeg']


#Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
db = SQLAlchemy(app)

class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))
    password = db.Column(db.String(80))


class user3(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	degree = db.Column(db.String(100))
	branch = db.Column(db.String(100))
	year = db.Column(db.Integer)
	subject = db.Column(db.String(100))
	def __repr__(self):
		return 'user3' + str(self.id)

@app.route("/")
def index3():
    return render_template("index3.html")

@app.route("/login",methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uname = request.form["uname"]
        passw = request.form["passw"]
        
        login = user.query.filter_by(username=uname, password=passw).first()
        if login is not None:
            return redirect(url_for("atten"))
    return render_template("login.html")
# @app.route('/forgot', methods=['GET','POST'])
# def forgot():
# 	ifrequest.method=='POST'
# 	uname = request.form['uname']
# 	reset = user.query.filter_by(username=uname, password= password).first()
# 	return render_template('forgot.html')
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        uname = request.form['uname']
        mail = request.form['mail']
        passw = request.form['passw']

        register = user(username = uname, email = mail, password = passw)
        db.session.add(register)
        db.session.commit()

        return redirect(url_for("login"))
    return render_template("register.html")
###############################################################################
@app.route("/atten", methods=["GET", "POST"])
def atten():
	if request.method == "POST":
		degr = request.form['degr']
		bran = request.form['bran']
		yer = request.form['yer']
		sub = request.form['sub'] 
		
		atten = user3( degree= degr, branch = bran, year = yer, subject = sub)
		db.session.add(atten)
		db.session.commit()
		return redirect(url_for("camera"))
	return render_template("attendance.html")
#################################################################################	
db.create_all()

@app.route('/list')
def list():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from user")
   
   rows = cur.fetchall(); 
   return render_template("list.html",rows = rows)
@app.route('/list2')
def list2():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from user3")
   
   rows = cur.fetchall(); 
   return render_template("list2.html",rows = rows)



@app.route('/camera')
def camera():
	return render_template('camera3.html')

@app.route('/compare', methods=['GET', 'POST'])
def compare_image():
	if request.method == 'POST':
		url = 'https://coeaifaceapi.herokuapp.com/face_rec'
		files = {'file': open('filename.jpg', 'rb')}
		resp = requests.post(url, files=files)
		#print(json.dumps(resp.json()))
		return json.dumps(resp.json(), skipkeys = True)
	else:
		return jsonify({'message': 'Something went wrong'})



if __name__=='__main__':
	app.run(debug = True)