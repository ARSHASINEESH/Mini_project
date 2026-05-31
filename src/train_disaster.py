#train_disaster.py
import pandas as pd
from sklearn.model_selection import train_test_split
from transformers import (
    DistilBertTokenizerFast,
    DistilBertForSequenceClassification,
    Trainer,
    TrainingArguments
)
from datasets import Dataset

df = pd.read_csv("data/bert_dataset.csv")

texts = df["text"].tolist()
labels = df["target"].tolist()

train_texts, val_texts, train_labels, val_labels = train_test_split(
    texts, labels, test_size=0.2, random_state=42
)

tokenizer = DistilBertTokenizerFast.from_pretrained(
    "distilbert-base-uncased"
)

train_encodings = tokenizer(train_texts, truncation=True, padding=True)
val_encodings = tokenizer(val_texts, truncation=True, padding=True)

train_dataset = Dataset.from_dict({
    **train_encodings,
    "label": train_labels
})

val_dataset = Dataset.from_dict({
    **val_encodings,
    "label": val_labels
})

model = DistilBertForSequenceClassification.from_pretrained(
    "distilbert-base-uncased",
    num_labels=2
)

training_args = TrainingArguments(
    output_dir="models/disaster_bert",
    num_train_epochs=8,
    per_device_train_batch_size=8,
    save_strategy="epoch"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset
)

trainer.train()
trainer.save_model("models/disaster_bert")
tokenizer.save_pretrained("models/disaster_bert")