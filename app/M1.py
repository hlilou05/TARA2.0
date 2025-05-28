from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Load GPT-Neo 1.3B
model_name = "EleutherAI/gpt-neo-1.3B"
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token  # 🔧 Fix for padding
model = AutoModelForCausalLM.from_pretrained(model_name)

def classify_cia(description):
    prompt = f"""You are a cybersecurity assistant. Based on the asset description, determine if each cybersecurity property is required.

Example:
Asset Description: The gateway ECU processes signals between external interfaces and internal CAN buses.
Confidentiality: Yes
Integrity: Yes
Availability: Yes

Now analyze the following asset:

Asset Description: {description}
Confidentiality:"""

    inputs = tokenizer(prompt, return_tensors="pt", padding=True, return_attention_mask=True)
    outputs = model.generate(
        input_ids=inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        max_length=inputs["input_ids"].shape[1] + 30,
        do_sample=False,
        temperature=0.3,
        eos_token_id=tokenizer.eos_token_id
    )

    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print("=== RAW OUTPUT ===")
    print(result)

    # Extract answers from generated text
    lines = result.split("\n")
    answers = {"Confidentiality": "Unknown", "Integrity": "Unknown", "Availability": "Unknown"}

    for i, line in enumerate(lines):
        for key in answers:
            if line.strip().startswith(f"{key}:"):
                val = line.split(":")[1].strip().capitalize()
                if val in ["Yes", "No"]:
                    answers[key] = val

    return answers

desc = "This ECU handles braking control and communicates with wheel sensors to adjust torque in real-time."

cia = classify_cia(desc)
print(cia)
# {'Confidentiality': 'Yes', 'Integrity': 'Yes', 'Availability': 'Yes'}
