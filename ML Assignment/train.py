import argparse
import os
import wandb
import torch
from transformers import Trainer, TrainingArguments
from model import init_model
from huggingface_hub import notebook_login


parser = argparse.ArgumentParser()
parser.add_argument('-n', '--num_samples', type=int, default=50000, help='Number of samples to use for fine-tuning the model')
args = parser.parse_args()
num_samples = args.num_samples


wandb.login()
notebook_login()
os.environ["WANDB_PROJECT"] = "python_code_lora"

def train(num_samples):
    model, tokenizer, tokenized_datasets, data_collator = init_model(num_samples)

    training_args = TrainingArguments(
        output_dir="YOUR OUTPUT DIR",
        per_device_train_batch_size=4,
        per_device_eval_batch_size=4,
        evaluation_strategy="epoch",
        logging_steps=25,
        num_train_epochs=1,
        learning_rate=1e-3,
        save_steps=100,
        report_to="wandb",
        gradient_accumulation_steps=4,
        fp16=True
    )

    trainer = Trainer(
        model=model,
        tokenizer=tokenizer,
        args=training_args,
        data_collator=data_collator,
        train_dataset=tokenized_datasets["train"],
        eval_dataset=tokenized_datasets["valid"]
    )

    trainer.train()
    trainer.push_to_hub()
    wandb.finish()

if __name__ == "__main__":
    train(num_samples)
