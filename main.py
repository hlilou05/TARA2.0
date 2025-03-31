import openpyxl

def modify_excel(file_path, modifications, save_as=None):
    """
    Modifies specific cells in an Excel file.

    :param file_path: Path to the Excel file.
    :param modifications: Dictionary with keys as cell coordinates (e.g., "A1") and values as new data.
    :param save_as: Optional new file name. If None, overwrites the original file.
    """
    # Load the workbook and select the active sheet
    wb = openpyxl.load_workbook(file_path)
    sheet = wb.active

    # Apply modifications
    for cell, value in modifications.items():
        sheet[cell] = value

    # Save changes
    save_path = save_as if save_as else file_path
    wb.save(save_path)
    print(f"Modifications saved to {save_path}")

# Example Usage
if __name__ == "__main__":
    excel_file = "input.xlsx"
    
    # Define modifications: Change A1 to "Hello", B2 to 123, and C3 to "Updated"
    modifications = {
        "A1": "Hello",
        "B2": 123,
        "C3": "Updated"
    }

    modify_excel(excel_file, modifications, save_as="modified.xlsx")
