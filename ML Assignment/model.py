from datasets import load_dataset, DatasetDict
from peft import LoraConfig, get_peft_model
from transformers import AutoTokenizer, GPT2LMHeadModel, DataCollatorForLanguageModeling
import torch

def init_model(num_samples):
    
    torch.manual_seed(42)

    # Loading the dataset
    dataset = load_dataset("ArtifactAI/arxiv_python_research_code")
    dataset_train = dataset["train"]

    # Preparing datasets for training and validation
    split_datasets = DatasetDict({
        "train": dataset_train.shuffle(seed=42).select(range(num_samples)),
        "valid": dataset_train.shuffle(seed=42).select(range(500))
    })

    # Loading tokenizer
    tokenizer = AutoTokenizer.from_pretrained("huggingface-course/code-search-net-tokenizer")
    context_length = 256

    # Tokenization function
    def tokenize_data(batch):
        outputs = tokenizer(
            batch["code"],
            truncation=True,
            max_length=context_length,
            return_overflowing_tokens=True,
            return_length=True
        )
        batch_input_ids = [
            input_ids for length, input_ids in zip(outputs["length"], outputs["input_ids"]) if length == context_length
        ]
        return {"input_ids": batch_input_ids}

    # Tokenizing datasets
    tokenized_datasets = split_datasets.map(tokenize_data, batched=True, remove_columns=split_datasets["train"].column_names)

    # Loading model
    model = GPT2LMHeadModel.from_pretrained("gpt2")

    # Applying LoRA
    lora_config = LoraConfig(
        r=8,
        lora_alpha=32,
        target_modules=["c_attn", "c_proj"],  # Targeting the Conv1D layers in GPT-2
        lora_dropout=0.1,
        bias="none",
    )
    model = get_peft_model(model, lora_config)

    # Preparing the data collator with labels
    tokenizer.pad_token = tokenizer.eos_token
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer, mlm=False, return_tensors="pt"
    )

    return model, tokenizer, tokenized_datasets, data_collator
