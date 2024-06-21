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
    
    #print(predictions, topic[:2])
    
    return map(int, predictions)

#new_data = ["привет как дела"]
#process_topic(new_data)

#def _parse_args():
#    parser = argparse.ArgumentParser(
#        description="Run text classification"
#    )
#    parser.add_argument(
#        "--intro", help="Path intro part of lesson"
#    )
#    parser.add_argument(
#        "--midle", help="Path midle part of lesson"
#   )
#    
#    parser.add_argument(
#        "--end", help="Path end of lesson"
#    )
#    
#    return parser.parse_args()

    

#if __name__ == "__main__":
#    args = _parse_args()
#    main(
#        intro=args.intro,
#        midle=args.midle,
#        end=args.end,
#    )