#!/usr/bin/python

#Functions for rendering html templates

from flask import Flask, render_template, request, redirect, url_for
from pcake import app
from models import *
import os
import time
from threading import Timer

#declare the app
app = Flask(__name__)

#find root directory
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():
	return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload():
	target = os.path.join(APP_ROOT, 'images/')
	if not os.path.isdir(target):
		os.mkdir(target)

	file = request.files['file']
	filename = file.filename
	destination = os.path.join(target, filename)
	#file.save(destination)

	predicted_class = predict(file)

	#time.sleep(1)
	return render_template('complete.html', predicted_class = predicted_class)

@app.route('/sample_index')
def sample_index():
	return render_template('samples.html')

@app.route('/upload_sample', methods=['POST'])
def upload_sample():
	target = os.path.join(APP_ROOT, 'static/img/')
	if request.form['action'] == 'Benchpress 1':
		filename = 'benchpress_sample_01.jpg'
	elif request.form['action'] == 'Benchpress 2':
		filename = 'benchpress_sample_02.jpg'
	elif request.form['action'] == 'Benchpress 3':
		filename = 'benchpress_sample_03.jpg'
	elif request.form['action'] == 'Hyperextension Bench 1':
		filename = 'hyperext-bench_sample_01.jpg'
	elif request.form['action'] == 'Hyperextension Bench 2':
		filename = 'hyperext-bench_sample_02.jpg'
	elif request.form['action'] == 'Hyperextension Bench 3':
		filename = 'hyperext-bench_sample_03.jpg'
	elif request.form['action'] == 'Leg Press 1':
		filename = 'leg-press_sample_01.jpg'
	elif request.form['action'] == 'Leg Press 2':
		filename = 'leg-press_sample_02.jpg'
	elif request.form['action'] == 'Leg Press 3':
		filename = 'leg-press_sample_03.jpg'
	elif request.form['action'] == 'Plyometric Box 1':
		filename = 'plyo-box_sample_01.jpg'
	elif request.form['action'] == 'Plyometric Box 2':
		filename = 'plyo-box_sample_02.jpg'
	elif request.form['action'] == 'Plyometric Box 3':
		filename = 'plyo-box_sample_03.jpg'
	elif request.form['action'] == 'Power Rack 1':
		filename = 'power-rack_sample_01.jpg'
	elif request.form['action'] == 'Power Rack 2':
		filename = 'power-rack_sample_02.jpg'
	elif request.form['action'] == 'Power Rack 3':
		filename = 'power-rack_sample_03.jpg'

	file = os.path.join(target, filename)
	predicted_class = predict(file)

	return render_template('complete.html', predicted_class = predicted_class)

#display 413
@app.errorhandler(413)
def page_not_found(e):
    return render_template('413.html'), 413
