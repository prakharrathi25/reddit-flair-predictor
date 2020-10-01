# Reddit Flair Prediction App: An end-to-end machine leanring Project

## Background 

**What are Reddit Flairs?**

A flair is a 'tag' that can be added to threads posted on the reddit website within a sub-reddit. They help users understand the category to which the posts they are scrolling through, belong and thus, help them filter out specific posts based on their preferences.

This is a web-app that I created that performs the task of predicting which flair should be alloted to a post. As a user, you just need to paste the link of the reddit post in the search bar. Find the webapp [here](https://flair-prediction-app.herokuapp.com/)

### Automated Testing 
The automated testing file can be found [here](https://automated-testing-endpoint.herokuapp.com/). You have to upload a .txt file followed by downloading a .json file with the required predictions. 

## Directory Structure 

I have made a flask app which is hosted on Heroku. The structure of the directory can be found here. 
* Notebooks:  1. Collecting 'India' subreddit data.ipynb : Data collection notebook
              2. Data Analysis.ipynb: Different Data Analysis Tasks 
              3. Flair_Prediction.ipynb: Model Development 
              
* requirements.txt: Containing the requirements need to run this project. 
* app.py : Contains the flask app
* inference.py : Inference Engine that runs the model and returns the predictions. 


## References

https://towardsdatascience.com/scraping-reddit-data-1c0af3040768

