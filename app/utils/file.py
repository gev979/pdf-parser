import os
import uuid

DIRECTORY = "storage/files"

# Ensure the PDF and result directories exist
os.makedirs(DIRECTORY, exist_ok=True)

async def upload(file):
    # Get the original filename
    original_filename = file.filename
    # Create a unique filename without the file extension for the folder
    base_filename, file_extension = os.path.splitext(original_filename)
    unique_folder_name = f"{base_filename}_{uuid.uuid4()}"
    file_location = os.path.join(DIRECTORY, unique_folder_name + file_extension)
    
    # Save the uploaded PDF file to the pdf directory
    with open(file_location, "wb") as pdf_file:
        pdf_file.write(await file.read())

    return file_location, unique_folder_name