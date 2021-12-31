import nltk
import json
import os.path
import numpy as np
from joblib import load
from nltk.corpus import stopwords
from flask import Flask, render_template, request
from db import create_movie_db, query_all, insert_review

nltk.download("stopwords")

model = load("DATA_X_pickle.joblib") 
vector = load("DATA_X_vector.joblib")

if not os.path.isfile("movie_review.db"):
    res = create_movie_db()
    print(res)

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home():
    """
    Home route
    """
    if request.method == "POST":
        # include code for feedback
        fb = request.form.to_dict()
        if "correct" in fb.keys():
            feedback = "CORRECT"
        elif "wrong" in fb.keys():
            feedback = "WRONG"
        data = fb["old_data"].replace("'", '"')
        data = json.loads(data)
        pred = data["pred"]
        review = data["user_review"]
        insert_review(review, pred, feedback)
    return render_template("home.html")


@app.route("/data")
def data():
    """
    Data route
    """
    data_obj = query_all()
    data = [i for i in data_obj]
    return render_template("data.html", data=data)
    

@app.route("/result", methods=["POST"])
def result():
    """
    result route
    """
    user_review = request.form["review"]
    review = user_review.lower().split()
    engStops = set(stopwords.words("english"))
    processed_review = [word for word in review if not word in engStops]
    processed_review = ' '.join(review)
    vectorised_review = vector.transform(np.array([processed_review]))
    prediction = model.predict(vectorised_review)[0]
    if prediction == 0:
        pred = "NEGATIVE"
    else:
        pred = "POSITIVE"
    data = dict()
    data["pred"] = pred
    data["user_review"] = user_review
    return render_template("result.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)
