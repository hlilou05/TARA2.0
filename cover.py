import json
import openpyxl
import getpass
from datetime import datetime

# === CONFIG ===
excel_file = "test.xlsm"
sheet_name = "Cover"
json_file = "project_data.json"
output_file = excel_file

# === Load JSON data ===
with open(json_file, "r") as f:
    data = json.load(f)

# === Load Excel workbook ===
wb = openpyxl.load_workbook(excel_file)

# === Select target sheet ===
if sheet_name in wb.sheetnames:
    sheet = wb[sheet_name]
else:
    raise ValueError(f"Sheet '{sheet_name}' not found in '{excel_file}'")

# === Hardcoded Mapping ===
# This is where you decide where each JSON value goes
if data["new_project"]:
    mapping = {
        "A1": data["source_folder"],
        "C4": data["project_name"],
        "C3": data["project_number"],
        "C11": getpass.getuser(),
        "A5": data["project_description"],
        "B27": "1.0",
        "C27": datetime.today().strftime('%d/%m/%Y')
        }
    
else:
    mapping = {
        "A1": data["source_folder"],
        "C11": getpass.getuser(),
        "A5": data["project"]
    }
# === Write to Excel ===
for cell, value in mapping.items():
    sheet[cell] = value

# === Save the workbook ===
wb.save(output_file)
print(f"✅ Excel file saved as {output_file}")
