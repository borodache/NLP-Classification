from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC

from utils import clean_text


class MyApp(App):
    def __init__(self, file_path: str = ".\subjects-questions.csv"):
        App.__init__(self)
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
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.2,
                                                                                random_state=1)
        self.tfidf_vectorizer = TfidfVectorizer(stop_words="english",
                                           preprocessor=clean_text,
                                           ngram_range=(1, 2))

        self.training_features_tfidf = self.tfidf_vectorizer.fit_transform(self.X_train)
        self.test_features_tfidf = self.tfidf_vectorizer.transform(self.X_test)

        # Training
        self.model = LinearSVC()
        self.model.fit(self.training_features_tfidf, self.y_train)

    def build(self):
        layout = BoxLayout(padding=10, orientation='vertical')
        self.txt1 = TextInput(text='', multiline=False)
        layout.add_widget(self.txt1)
        btn1 = Button(text="Submit")
        btn1.bind(on_press=self.buttonClicked)
        layout.add_widget(btn1)
        self.label1 = Label(text=self.output, color=[50, 50, 50, 50])
        # self.lbl1.color = 'white'
        layout.add_widget(self.label1)

        return layout

# button click function
    def buttonClicked(self, btn):
        tfidf_features = self.tfidf_vectorizer.transform([self.txt1.text])
        self.output = self.model.predict(tfidf_features)[0]
        self.label1.text = self.output
        # self.build()


# if __name__ == '__main__':
MyApp().run()
