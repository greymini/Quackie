# GPT-2 Fine-Tuning and Quantization for Python Code Generation

This project fine-tunes GPT-2 on a Python code dataset, quantizes the model, and then generates Python code based on input prompts.

## Files

- `train.py`: Fine-tunes the GPT-2 model on a Python code dataset.
- `model.py`: Defines the model loading, configuration, and quantization.
- `predict.py`: Generates Python code using the quantized model.
- `requirements.txt`: Lists required Python packages.
- `README.md`: Project documentation.

## Setup

1. Clone the repository.

   git clone https://github.com/greymini/Quackie.git
   cd Quackie

2. Install the necessary packages.

   pip install -r requirements.txt

3. Login to Weights & Biases and Hugging Face Hub.

   wandb.login()
   huggingface-cli login

## Training: You need to run the train.py script to finetune the model
   
   python train.py

## Predicition: After fine-tuning, use the predict.py script to generate Python code based on prompts

   python predict.py


## Link to the model on Hugging Face Hub is:
   https://huggingface.co/phoenix28/python_code_lora

## I also want to inform you that I finetuned GPT2 using Pytorch Trainer and it has lower loss than the one trained using LoRA, I am also adding the link to that and the notebook in which I trained it. I could not quantize that model so I haven't added the scripts reagrding that model.

   https://huggingface.co/phoenix28/python_code_gen

