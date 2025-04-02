import customtkinter as ctk
from tkinter import filedialog
import json
import subprocess

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Project Setup")
app.geometry("500x450")
app.configure(fg_color="#009B9B")

def browse_folder():
    folder_selected = filedialog.askdirectory()
    folder_entry.delete(0, "end")
    folder_entry.insert(0, folder_selected)

def start_action():
    # Collect variables
    data = {
        "source_folder": folder_entry.get(),
        "project_name": project_name_entry.get(),
        "project_number": project_number_entry.get(),
        "new_project": new_project_var.get(),
        "project_description": project_description_entry.get("1.0", "end").strip()
    }
    
    # Save to JSON
    with open("project_data.json", "w") as f:
        json.dump(data, f)
    
    # Launch next script
    subprocess.Popen(["python", "cover.py"])  # Make sure next_script.py exists
    
    # Optionally close the GUI
    app.destroy()

# ----------------- GUI -----------------
ctk.CTkLabel(app, text="Select Your Source Folder", text_color="white").place(x=30, y=30)
folder_entry = ctk.CTkEntry(app, width=280)
folder_entry.place(x=30, y=55)
ctk.CTkButton(app, text="Browse", command=browse_folder, corner_radius=15).place(x=320, y=54)

ctk.CTkLabel(app, text="Project Name", text_color="white").place(x=30, y=95)
project_name_entry = ctk.CTkEntry(app, width=400)
project_name_entry.place(x=30, y=120)

ctk.CTkLabel(app, text="Project Number", text_color="white").place(x=30, y=155)
project_number_entry = ctk.CTkEntry(app, width=400)
project_number_entry.place(x=30, y=180)

new_project_var = ctk.BooleanVar()
ctk.CTkLabel(app, text="New Project", text_color="white").place(x=30, y=215)
ctk.CTkCheckBox(app, variable=new_project_var, text="").place(x=140, y=215)

ctk.CTkLabel(app, text="Project Description", text_color="white").place(x=30, y=245)
project_description_entry = ctk.CTkTextbox(app, width=400, height=80)
project_description_entry.place(x=30, y=270)

ctk.CTkButton(app, text="Start", command=start_action, corner_radius=25, width=80).place(x=210, y=370)

app.mainloop()
