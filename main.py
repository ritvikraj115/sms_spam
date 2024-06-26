import nltk
from nltk.corpus import stopwords
import string
import streamlit as st
import pickle
from nltk.stem.porter import PorterStemmer

ps = PorterStemmer()
tfidf = pickle.load(open('vectorizer.pkl', 'rb'))
model = pickle.load(open('model.pkl', 'rb'))


def transform_text(text):
    text = text.lower()
    nltk.download('punkt')
    nltk.download('stopwords')
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)
    text = y[:]
    y.clear()
    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)
    text = y[:]
    y.clear()
    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)


st.title('Email/SMS Spam Classifier')

input_sms = st.text_area('Enter the message')
if st.button('Predict'):
    transformedsms = transform_text(input_sms)

    vector_input = tfidf.transform([transformedsms])

    result = model.predict(vector_input)[0]

    if result == 1:
        st.header("Spam")
    else:
        st.header('Not spam')
