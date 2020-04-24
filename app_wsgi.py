''' Importing necessary libraries'''
from flask import Flask, render_template, url_for, request, redirect
from flask_bootstrap import Bootstrap
import os
import joblib

import inference

# Creating an instance of the flask app
app = Flask(__name__)
Bootstrap(app) # Pass app into the bootstrap Class to use Bootstrap functions


# Import our model
model = joblib.load('final_model.sav')
'''
ROUTES
'''
# Route when we recieve a GET or POST request
@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'GET':
        # Render the index page
        return render_template('index.html')

    # when the url has been submitted
    if request.method == 'POST':

        # Extract the URL
        text = request.form['url']

        # Check if the URL belongs to India subreddit
        if 'india' not in text:
            result = {
            'flair': "This does not belong to the subreddit 'India'",
            }
            return render_template('show.html', result=result)

        if text != ' ': # check if the click was valid

            # ''' ADD URL validation here '''

            # Get the predsicted class name from the inference module function
            flair_type = inference.get_flair(url=text, loaded_model=model)
            flair_type = list(flair_type)[0]
            print('The following post belongs to : {}'.format(flair_type)) # Display the result

            # Result to be displayed
            result = {
            'flair': flair_type,
            }
        return render_template('show.html', result=result)


if __name__ == '__main__':
    app.run(debug=True)
