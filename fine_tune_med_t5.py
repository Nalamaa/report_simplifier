print("Script started...")  # Add at the top of fine_tune_med_t5.py

from transformers import T5Tokenizer, T5ForConditionalGeneration, Trainer, TrainingArguments, DataCollatorForSeq2Seq
from datasets import load_dataset

# Name of the base model and dataset
MODEL_NAME = "t5-small"
DATASET_NAME = "liliya-makhmutova/medical_texts_simplification"

# Load the tokenizer and model
tokenizer = T5Tokenizer.from_pretrained(MODEL_NAME)
model = T5ForConditionalGeneration.from_pretrained(MODEL_NAME)

# Load the dataset
dataset = load_dataset(DATASET_NAME)

# Preprocess: for T5, add 'simplify: ' prefix, tokenize input/target
def preprocess(batch):
    prefix = "simplify: "
    inputs = [prefix + text for text in batch["original"]]
    targets = batch["human_simplification"]
    model_inputs = tokenizer(inputs, max_length=128, truncation=True, padding="max_length")
    labels = tokenizer(targets, max_length=128, truncation=True, padding="max_length")
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

tokenized = dataset.map(preprocess, batched=True)

# Training arguments
args = TrainingArguments(
    output_dir="medt5-simplified",
    evaluation_strategy="epoch",
    num_train_epochs=3,
    per_device_train_batch_size=8,
    save_total_limit=1,
    report_to="none"
)

# Data collator
collator = DataCollatorForSeq2Seq(tokenizer, model=model)

# Trainer
trainer = Trainer(
    model=model,
    args=args,
    train_dataset=tokenized["train"],
    eval_dataset=tokenized["validation"],
    data_collator=collator,
    tokenizer=tokenizer
)

# Fine-tune
trainer.train()
# Save your model and tokenizer for later use in FastAPI
model.save_pretrained("medt5-simplified")
tokenizer.save_pretrained("medt5-simplified")
