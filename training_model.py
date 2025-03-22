import json
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Trainer, TrainingArguments
from datasets import Dataset, DatasetDict

# Load dataset from JSON file
with open('prompts.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Convert data to Hugging Face Dataset format
dataset = Dataset.from_dict(data)

# Load pre-trained model and tokenizer
model_name = "t5-small"  # Example: T5 small model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Tokenize data
def preprocess_function(examples):
    inputs = examples['question']
    targets = examples['answer']
    model_inputs = tokenizer(inputs, padding=True, truncation=True, return_tensors="pt")
    with tokenizer.as_target_tokenizer():
        labels = tokenizer(targets, padding=True, truncation=True, return_tensors="pt")
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

# Preprocess and tokenize dataset
tokenized_datasets = dataset.map(preprocess_function, batched=True)

# Training arguments
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["test"],
)

# Train the model
trainer.train()

# Save trained model and tokenizer
model.save_pretrained("./trained_model")
tokenizer.save_pretrained("./trained_model")
