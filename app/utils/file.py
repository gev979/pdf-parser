import os

import os


async def upload(file, directory):
    try:
        # Get the original filename
        original_filename = file.filename
        # Create a unique filename without the file extension for the folder
        base_filename, file_extension = os.path.splitext(original_filename)

        dirc = os.path.join(directory, base_filename)
        os.makedirs(dirc, exist_ok=True)
        file_location = os.path.join(dirc, "file" + file_extension)

        # Save the uploaded PDF file to the pdf directory
        with open(file_location, "wb") as pdf_file:
            pdf_file.write(await file.read())

        return file_location, base_filename

    except Exception as e:
        # Log or handle the error (logging is a good practice in production)
        print(f"Error during file upload: {e}")
        # Return None if there's an error
        return None
