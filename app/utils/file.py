import os
import uuid

async def upload(file, directory):
    # Get the original filename
    original_filename = file.filename
    # Create a unique filename without the file extension for the folder
    base_filename, file_extension = os.path.splitext(original_filename)
    unique_folder_name = f"{base_filename}_{uuid.uuid4()}"

    dir = os.path.join(directory, unique_folder_name)
    os.makedirs(dir, exist_ok=True)
    file_location = os.path.join(dir, "file" + file_extension)
    
    # Save the uploaded PDF file to the pdf directory
    with open(file_location, "wb") as pdf_file:
        pdf_file.write(await file.read())

    return file_location, unique_folder_name