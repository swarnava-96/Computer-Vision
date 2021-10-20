# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 12:02:43 2021

@author: SWARNAVA
"""

# Importing the dependencies
from flask import Flask, render_template, Response
import cv2

# Lets initialize the flask app
app = Flask(__name__)

# Lets capture live webcam recordings
camera = cv2.VideoCapture(0)

# Lets define a function for capturing the video frames and converting into bytes and sending to the front end
def generate_frames():
    while True:
        # Reading the camera frames
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode(".jpg", frame)
            frame = buffer.tobytes()
            
        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
# Lets set the homepage
@app.route("/")
def index():
    return render_template("index.html")

# Lets set the video page
@app.route("/video")
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)