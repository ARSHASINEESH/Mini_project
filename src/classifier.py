#classifier.py
import torch
import joblib
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification

tokenizer = DistilBertTokenizer.from_pretrained("models/disaster_bert")
bert_model = DistilBertForSequenceClassification.from_pretrained("models/disaster_bert")
bert_model.eval()

help_model, vectorizer = joblib.load("models/help_model.pkl")


def predict_disaster(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = bert_model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=1)
    return probs[0][1].item()


def predict_help(text):
    vec = vectorizer.transform([text])
    return help_model.predict_proba(vec)[0][1]