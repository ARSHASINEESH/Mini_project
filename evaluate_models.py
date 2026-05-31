import os
import pandas as pd
import torch
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification


# =========================
# 1. BERT MODEL EVALUATION
# =========================
print("\n========== BERT MODEL EVALUATION ==========\n")

bert_df = pd.read_csv("data/bert_dataset.csv")

bert_texts = bert_df["text"].tolist()
bert_true_labels = bert_df["target"].tolist()

tokenizer = DistilBertTokenizer.from_pretrained("models/disaster_bert")
bert_model = DistilBertForSequenceClassification.from_pretrained("models/disaster_bert")
bert_model.eval()

bert_predictions = []

for text in bert_texts:
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = bert_model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=1)
        pred = torch.argmax(probs, dim=1).item()
    bert_predictions.append(pred)

print("Classification Report (BERT):\n")
print(classification_report(bert_true_labels, bert_predictions))

bert_acc = accuracy_score(bert_true_labels, bert_predictions)
print("Accuracy (BERT):", bert_acc)

bert_cm = confusion_matrix(bert_true_labels, bert_predictions)
print("Confusion Matrix (BERT):\n")
print(bert_cm)

plt.figure(figsize=(8, 6))
sns.heatmap(
    bert_cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=["Non-Disaster", "Disaster"],
    yticklabels=["Non-Disaster", "Disaster"]
)
plt.title("BERT Confusion Matrix")
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.tight_layout()
plt.savefig(os.path.join(os.getcwd(), "bert_confusion_matrix.png"))
plt.show()
plt.clf()


# =========================
# 2. HELP MODEL EVALUATION
# =========================
print("\n========== HELP MODEL EVALUATION ==========\n")

help_df = pd.read_csv("data/loreg_dataset.csv")

help_texts = help_df["text"].tolist()
help_true_labels = help_df["help_label"].tolist()

help_model, vectorizer = joblib.load("models/help_model.pkl")

X_help = vectorizer.transform(help_texts)
help_predictions = help_model.predict(X_help)

print("Classification Report (Help Model):\n")
print(classification_report(help_true_labels, help_predictions))

help_acc = accuracy_score(help_true_labels, help_predictions)
print("Accuracy (Help Model):", help_acc)

help_cm = confusion_matrix(help_true_labels, help_predictions)
print("Confusion Matrix (Help Model):\n")
print(help_cm)

plt.figure(figsize=(8, 6))
sns.heatmap(
    help_cm,
    annot=True,
    fmt="d",
    cmap="Greens",
    xticklabels=["No Help", "Help"],
    yticklabels=["No Help", "Help"]
)
plt.title("Help Model Confusion Matrix")
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.tight_layout()
plt.savefig(os.path.join(os.getcwd(), "help_confusion_matrix.png"))
plt.show()
plt.clf()


# =========================
# 3. ACCURACY BAR GRAPH
# =========================
plt.figure(figsize=(8, 6))
plt.bar(["BERT Model", "Help Detection Model"], [bert_acc, help_acc])
plt.title("Model Accuracy Comparison")
plt.xlabel("Models")
plt.ylabel("Accuracy Score")
plt.ylim(0, 1)
plt.tight_layout()
plt.savefig(os.path.join(os.getcwd(), "accuracy_comparison.png"))
plt.show()
plt.clf()


# =========================
# 4. SAVE LOCATION
# =========================
print("\nImages saved in:", os.getcwd())
print("Saved files:")
print("- bert_confusion_matrix.png")
print("- help_confusion_matrix.png")
print("- accuracy_comparison.png")