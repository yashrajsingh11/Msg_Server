# Msg_Server
## Overview
A Flutter Mobile Application with a backend Flask server that automatically scans through incoming SMS texts for URLs and detects possible phishing attacks. 
## Features
1) It sends the URLs to the server, which contains a pre-trained model for detecting phishing websites. 
2) The server runs the model on the URL and returns the predicted output to the application.
3) The message is displayed in RED if it is a possible phishing link, else it is displayed in GREEN.
4) Users have the option to give feedback for the predicted output, in case it was wrong. 
5) They can report it to the concerned authority as well. 
## Sample Screenshots
![Alt text](Images/1.png?raw=true "Result1")
![Alt text](Images/2.png?raw=true "Result2")
![Alt text](Images/3.png?raw=true "Result3")
![Alt text](Images/4.png?raw=true "Result4")
## Github Links:
1) Flutter Frontend: https://github.com/yashrajsingh11/Msg_App
2) Flask Backend Server: https://github.com/yashrajsingh11/Msg_Server
## Instructions:
### For Starting Server:
1) First Create Virtual Environment using the command virtualenv env in the terminal
2) Activate Virtual Environment using command env\Scripts\activate in the terminal
3) Run command pip install -r requirements.txt
4) Run the Server using the command python app.py in the terminal
### For Starting Flutter Application: 
Run the Flutter Application on Emulator
## Future Scope
1) This system can be hosted on a cloud platform where it can process data and user feedback in a Machine Learning Pipeline to give more accurate real-time predictions, increasing its reliability and adaptability.
2) It can be modified to work as an API service, then it can be attached to a variety of web and mobile applications which require this kind of system.
## Bibliography
### Dataset: 
https://www.kaggle.com/shashwatwork/web-page-phishing-detection-dataset
### Research Papers: 
1) https://www.researchgate.net/publication/328541785_Phishing_Website_Detection_using_Machine_Learning_Algorithms

2) https://www.ijert.org/detection-of-phishing-websites-using-machine-learning
