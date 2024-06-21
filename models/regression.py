# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 11:49:01 2024

@author: M
"""
import argparse
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

MODEL_PATH = './models/logistic_regression_model.pkl'
VECTORIZER_PATH = './models/tfidf_vectorizer.pkl'

def load_model(v_path, m_path):
    model = joblib.load(m_path)
    vectorizer = joblib.load(v_path)
    return model, vectorizer

def process_topic(topic):
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    new_data_tfidf = vectorizer.transform(topic)
    predictions = model.predict(new_data_tfidf)
    
    return map(int, predictions)
