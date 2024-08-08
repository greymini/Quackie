import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

def generate_output(prompt):
    model_id = "phoenix28/python_code_lora"
    tokenizer = AutoTokenizer.from_pretrained(model_id, use_fast=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        device_map="auto",
        trust_remote_code=False,
        revision="main"
    )

    # Creating a pipeline
    pipe = pipeline(model=model, tokenizer=tokenizer, task='text-generation')

    # Generating output
    outputs = pipe(
        prompt,
        max_new_tokens=50,
        do_sample=True,
        temperature=0.7,
        top_k=50,
        repetition_penalty=2.0
    )
    return outputs[0]["generated_text"]

if __name__ == "__main__":
    #Example prompt(Can be chnaged)
    prompt = """
    # create some data
    x = np.random.randn(100)
    y = np.random.randn(100)

    # create scatter plot with x, y
    """
    print(generate_output(prompt))
