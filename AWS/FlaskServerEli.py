from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from datetime import datetime

from utils import clean_text
from logger import logger

#DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
bootstrap = Bootstrap(app)


class Model:
    def __init__(self,
                 file_path: str = "/home/ubuntu/nlp-classification/subjects-questions.csv"):
                 # file_path: str = r"C:\Users\borod\OneDrive\Documents\Projects\NLP Classification Science Themes AWS\subjects-questions.csv"):
        # App.__init__(self)
        self.output = ''
        self.file_path = file_path
        self.df = pd.read_csv(self.file_path, header=None, usecols=[0, 1], names=['question', 'category'])
        # prepare data
        self.df = self.df[self.df['category'].isin(['Physics', 'Chemistry', 'Maths', 'Biology'])]
        self.questions = self.df['question']
        self.new_questions = []
        for question in self.questions:
            self.new_questions.append(clean_text(question))

        self.X = self.new_questions
        self.y = self.df['category']
        self.tfidf_vectorizer = TfidfVectorizer(stop_words="english",
                                                preprocessor=clean_text,
                                                ngram_range=(1, 2))

        self.training_features_tfidf = self.tfidf_vectorizer.fit_transform(self.X)

        # Training
        self.model = LinearSVC()
        self.model.fit(self.training_features_tfidf, self.y)

    def predict(self, text):
        tfidf_features = self.tfidf_vectorizer.transform([text])

        return self.model.predict(tfidf_features)[0]


class NameForm(FlaskForm):
    word = StringField('Your sentence?', validators=[DataRequired()])
    submit = SubmitField('Submit')
 #   category = StringField('Category')


@app.route("/", methods=['GET', 'POST'])
def index():
    category = ""
    word = ""
    form = NameForm()
    if request.method == 'POST':
        word = request.form["word"]
        category = get_category(word)
        # logger.log(
        logger.info(f"{datetime.now()}: {request.remote_addr} - {word} - {category}")
#        form.category = category
    ret = render_template('index.html', category=category, form=form)

    return ret


#@app.route("/", methods=['GET'])
#def index():
#    form = NameForm()
#    category = ""
#    if form.validate_on_submit():
#        word = form.word.data
#        category = get_category(word)
#        ret = render_template('index.html', category=category, form=form)
#    else:
#    ret = on_get_index()
#    return ret


def on_get_index():
    ret = """<title> Reusable Form Demo </title>
    <form action=\"\" method=\"post\">
    <div class =\"input text\">
    <label for=\"name\">Name:</label> <input id=\"name\" name=\"name\" required type=\"text\" value=\"\">
    </div>
    <div class=\"input submit\">
    <input type=\"submit\" value=\"Submit\">
    </div>
    </form>"""

    return ret


model = Model()


def get_category(text):
    return model.predict(text)


if __name__ == "__main__":
    print('Serving on port 18001...')
    # app.run(host="127.0.0.1", port=18001, debug=True)
#    app.run(host="172.31.28.172", port=18001, debug=True)
    app.run(host="172.31.28.172", port=18001)

