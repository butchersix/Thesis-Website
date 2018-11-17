from flask import Flask, request, render_template, jsonify
import pickle
import numpy as np

import warnings
import pandas as pd
import pickle
import os
import csv
import decimal
import shutil

allClass = [ 'background', 'aeroplane', 'bicycle', 'bird', 'boat',
			 'bottle', 'bus', 'car', 'cat', 'chair', 'cow', 'diningtable', 'dog',
			 'horse', 'motorbike', 'person', 'potted plant', 'sheep', 'sofa', 'train',
			 'tv/monitor']

items = []
folders = ['AMBIGUOUS', 'anger', 'anticipation', 'disgust', 'fear', 'joy', 'sadness', 'surprise', 'trust']
colorKeywords = ['Red', 'Yellow', 'Green', 'Cyan', 'Blue', 'Magenta']
columns = []
columns.append('filename')
columns.extend(allClass)

# Extend color to columns.
for color in colorKeywords:
	columns.append(color)
	columns.append('n_' + color.lower())

columns.append('emotion')
row = []

def generate(logfile):
	global allClass
	global row
	# ds = input('Directory path: ')
	
	file = logfile
	filename = os.fsdecode(file)
	fn = filename[:-4]
	currentRow = [0] * len(columns)
	currentRow[0] = fn
	# checkFile = open(os.getcwd()+'\\output_new_instances\\'+filename+'.log')
	checkFile = open('static/output_new_instances/'+filename+'.log')
	lines = checkFile.readlines()
	
	# Iterate allClass.
	for line in lines:
		# In label list.
		if any(classes in line for classes in allClass):
			currentLine = line.split()
			cl = currentLine[2]
			currentLabel = cl[:-1]
			currentValue = currentLine[3]
			index = columns.index(currentLabel)
			currentRow[index] = currentValue
		# In color family list.
		elif any(cfamily in line for cfamily in colorKeywords):
			currentLine = line.split()
			cf = currentLine[0]
			currentFamily = cf[:-1]
			currentPercentage = currentLine[1]
			numberOfInstances = currentLine[3]
			index = columns.index(currentFamily)
			currentRow[index] = currentPercentage
			index = columns.index('n_' + currentFamily.lower())
			currentRow[index] = numberOfInstances
		# Not matching any keywords.
		else:
			continue
	emotionOfPainting = getEmotionLabel(filename)
	indexOfEmotion = columns.index('emotion')
	currentRow[indexOfEmotion] = emotionOfPainting
	row.append(currentRow)

	createFile()

def createFile():
	# filename = input('Enter new name: ')
	filename = "emotions"
	# Change to desired output directory.
	# mainDirectory = r'C:\\Users\\Jasper\\Documents\\College\\Thesis\\Thesis II - Demo\\demo2\\'
	# mainDirectory = os.getcwd()

	# Create file.
	# originally having 'mainDirectory+'.csv'
	with open(filename+'.csv', 'w', newline='') as file:
		wr = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		cl = [x.lower() for x in columns]
		wr.writerow(cl)

		for rows in row:
			wr.writerow(rows)
		print('CSV created!')

def getEmotionLabel(painting):
	# Code here for getting the annotated emotion and append it to row.
	global items
	global folders
	i = 0
	for x in items:
		temp = [w.replace('.jpg', '.log') for w in x]
		# print(temp)
		if painting in temp:
			return folders[i]
		i = i + 1
	return ''


# FLASK PART

app = Flask(__name__)
# , static_url_path='', static_folder='/static', template_folder='/templates'

@app.route("/")
def home():
	return render_template("index.html")

@app.route("/getInterpretation", methods=['GET', 'POST'])
def getInterpretation():
	logfile = request.form['logfile']
	warnings.simplefilter("ignore", UserWarning)
	warnings.simplefilter("ignore", category=PendingDeprecationWarning)

	# print("Loading models...")
	# base-only rfc model
	rfc_bo_1_file = "final_ssl_rf_1.0.pickle"
	rfc_bo_1 = pickle.load(open(rfc_bo_1_file, "rb"))

	# base-iteration rfc model
	rfc_bi_2_file = "final_ssl_rf_2.0.pickle"
	rfc_bi_2 = pickle.load(open(rfc_bi_2_file, "rb"))

	# os.system('cls')
	# print("Successfully loaded models.\n")
	generate(logfile)
	emotion_input = 'emotions.csv'
	# emotion_input = "emotions.csv"
	emotion = pd.read_csv(emotion_input)

	# split emotion data to X and y
	emotion_o = emotion.copy()
	emotion = emotion.drop("filename", axis=1)
	num = len(emotion)
	X_emotion = emotion.drop('emotion', axis=1)
	y_emotion = emotion['emotion']

	# prediction of top 1 base-only model
	list_ = list(emotion_o['filename'])
	predictions = []
	for idx, val in enumerate(list_):

	# 	print("Prediction of {} from the top 1 base-only model: {}".format(val, rfc_bo_1.predict(X_emotion[idx:idx+1])))

	# 	# prediction of base-iteration model
	# 	print("Prediction of {} from the base-iteration model: {}\n".format(val, rfc_bi_2.predict(X_emotion[idx:idx+1])))
		predictions = [rfc_bo_1.predict(X_emotion[idx:idx+1])[0], rfc_bi_2.predict(X_emotion[idx:idx+1])[0]]
		# predictions = list(map(str, predictions))
	# print("\nPress any button to exit...")
	# prediction = [ada.predict(instance)[0], rfc.predict(instance)[0], svm.predict(instance)[0]]
	return jsonify(predictions=predictions)
	
if __name__ == '__main__':	
	app.run(debug=True)