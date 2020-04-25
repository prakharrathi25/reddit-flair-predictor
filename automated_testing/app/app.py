''' Importing necessary libraries'''
from flask import Flask, flash, render_template, url_for, request, redirect
from flask_bootstrap import Bootstrap
import os
import joblib
import json

import inference

# Creating an instance of the flask app
app = Flask(__name__)
Bootstrap(app) # Pass app into the bootstrap Class to use Bootstrap functions

# Import our model
model = joblib.load('final_model.sav')

links = []	# List to save the uploaded links

'''
ROUTES
'''
# Route when we recieve a GET or POST request
@app.route('/', methods=['GET', 'POST'])
def index():
	predictions = dict()	# Dictionary which will be converted to the json file

	# when the image has been uploaded
	if request.method == 'POST':

		# Check if the post request has a file
		if 'file' not in request.files:
			flash("No File Attached")
			return redirect(request.url)

		# Collect the uploaded file
		uploaded_file = request.files['file']
		print(request.files)
		if uploaded_file.filename != '': # check if the click was valid

			# Saving a copy of the uploaded file to static folder
			file_path = os.path.join('static', uploaded_file.filename)  # A unique filaneme creattion method can be used here
			uploaded_file.save(file_path)

			# File Reading
			try:
				f = open(file_path, 'r')
				links = f.readlines()
			except IOError:
				print("Could Not read file")

			# Get the predicted class name from the inference module function
			for url in links:

				# Check if it belongs to the India subreddit
				if '/india/' not in url:
					predictions[url] = "This thread does not belong to India subreddit"

				else:
					# Obtain the predicted flair type
					flair_type = inference.get_flair(url=url, loaded_model=model)
					flair_type = list(flair_type)[0]
					predictions[url] = flair_type

			# Save the output to a json file
			print(type(predictions))

			with open('static/predictions.json', 'w') as json_file:
				json.dump(predictions, json_file)

			return render_template('show.html')
	return render_template('index.html')

if __name__ == '__main__':
	app.run(debug=True)
