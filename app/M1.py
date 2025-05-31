from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

model_name = "EleutherAI/gpt-neo-1.3B"
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token  # to fix the padding
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
    #print("=== RAW OUTPUT ===")
    #print(result)

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
def generate_damage_scenario(cyber_property, description):
    prompt = f"""You are a cybersecurity risk analyst. Your task is to write a damage scenario involving a loss of {cyber_property.lower()} for the described asset.

Example:
Asset Description: The gateway ECU processes signals between external interfaces and internal CAN buses.
Cybersecurity Property: Confidentiality
Damage Scenario: Unauthorized access to gateway messages could leak sensitive vehicle communication data.

Now analyze the following asset:

Asset Description: {description}
Cybersecurity Property: {cyber_property}
Damage Scenario:"""

    inputs = tokenizer(prompt, return_tensors="pt", padding=True, return_attention_mask=True)
    outputs = model.generate(
        input_ids=inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        max_length=inputs["input_ids"].shape[1] + 50,
        do_sample=True,
        top_p=0.9,
        temperature=0.8,
        eos_token_id=tokenizer.eos_token_id
    )

    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    #print("=== RAW OUTPUT ===\n", result)

    # Extract the line that starts with "Damage Scenario:"
    for line in result.split("\n"):
        if line.strip().startswith("Damage Scenario:"):
            return line.split(":", 1)[1].strip()

    return "No scenario generated."

desc = "This ECU handles braking control and communicates with wheel sensors to adjust torque in real-time."

#cia = classify_cia(desc)
#print(cia)
#print("Confidentiality:", generate_damage_scenario("Confidentiality", desc))
x = 0
class AssetRiskProfile:
    def __init__(self, component, func, assetID, assetList, assetDesc):
        self.component = component
        self.func = func
        self.assetID = assetID
        self.assetList = assetList
        self.assetDesc = assetDesc

        # Auto-generate the rest
        self.classify_cia_properties()
        self.generate_damage_scenarios()

    def to_list(self):
        return [
            self.component, self.func, self.assetID, self.assetList, self.assetDesc,
            self.confidentiality, self.integrity, self.availability,
            self.idC, self.descC, self.idI, self.descI, self.idA, self.descA
        ]

    def classify_cia_properties(self):
        result = classify_cia(self.assetDesc)
        self.confidentiality = result["Confidentiality"]
        self.integrity = result["Integrity"]
        self.availability = result["Availability"]
  
    def transform_string(self, input_str):
        if "AS" in input_str:
            input_str = input_str.split("AS")[0]
        return input_str.strip() + f"DS_{x}"
   
    def generate_damage_scenarios(self):
        if self.confidentiality.lower() == "yes":
            self.idC = self.transform_string(self.assetID)
            self.descC = generate_damage_scenario("Confidentiality", self.assetDesc)
            X=+1
        else:
            self.idC = "N/A"
            self.descC = ""

        if self.integrity.lower() == "yes":
            self.idI = self.transform_string(self.assetID)
            self.descI = generate_damage_scenario("Integrity", self.assetDesc)
            X=+1
        else:
            self.idI = "N/A"
            self.descI = ""

        if self.availability.lower() == "yes":
            self.idA = self.transform_string(self.assetID)
            self.descA = generate_damage_scenario("Availability", self.assetDesc)
            X=+1
        else:
            self.idA = "N/A"
            self.descA = ""

asset = AssetRiskProfile(
    "ECU1", "Brake Control", "001", "ABS, TCS", "Manages braking and torque balance in real time."
)

print(asset.to_list())
