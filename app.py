from flask import Flask, request, render_template, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os
import json
import requests
import cv2
import warnings
import jsonify
warnings.filterwarnings("ignore")

app = Flask(__name__)

UPLOAD_FOLDER = 'received_files'
ALLOWED_EXTENSIONS = ['png','jpg','jpeg']

@app.route('/face', methods = ['GET','POST'])
def f_match():
	video = cv2.VideoCapture(0)
	while True:
		ret, frame = video.read()
		cv2.imshow("Capturing",frame)
		if cv2.waitKey(1) & 0xFF== ord('c'):
			break
		showPic = cv2.imwrite("filename.jpg",frame) 
	#video.release()
	cv2.destroyAllWindows
	#if request.method == 'POST':
	try:
		url = 'https://coeaifaceapi.herokuapp.com/face_rec'
		files = {'file': open('filename.jpg', 'rb')}
		resp = requests.post(url, files=files)
		#print(json.dumps(resp.json()))
		return json.dumps(resp.json(), skipkeys = True)
		#return jsonify({'message':json.dumps(resp.json())})
	except:
		return 'No face Matched '
	return '''
	<!doctype html>
	<title>Face Recognizer </title>
	<body>
		<a href='/face'></a>
	</body>
	'''

if __name__=='__main__':
	app.run(debug = True)