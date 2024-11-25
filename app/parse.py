import asyncio
import os
import io
import sys
import re
from fastapi import UploadFile
from parsers.pdf_marker import parse_with_pdf_marker

async def main():
    directory = "storage/test/files"
    try:
        os.makedirs(directory, exist_ok=True)
        pdf_files = [file for file in os.listdir(directory) if file.endswith('.pdf')]

        for pdf_file in pdf_files:
            pdf_path = os.path.join(directory, pdf_file)

            base_name = os.path.splitext(pdf_file)[0]  # Extract the base name (without extension)

            file_exist = False
            # Iterate through files in the folder
            for dirc in os.listdir("storage/results"):
                if base_name in dirc:
                    file_exist = True  # File exists with the given base name and a UUID
                    break

            if file_exist:
                continue

            print("Parsing", pdf_file)

            try:
                # Open the PDF file in binary mode
                with open(pdf_path, 'rb') as pdf_file_obj:
                    pdf_content = pdf_file_obj.read()

                    # Create a BytesIO object to simulate a file-like object
                    pdf_file_like = io.BytesIO(pdf_content)
                    pdf_file_like.name = pdf_file  # Set the filename attribute

                    # Create the UploadFile object
                    upload_file = UploadFile(filename=pdf_file, file=pdf_file_like)

                    # Now pass the UploadFile object to the parse_with_pdf_marker function
                    await parse_with_pdf_marker(upload_file)
                    # Process result here, if needed
            except Exception as e:
                print(f"Error parsing {pdf_file}: {e}")

    except OSError as os_error:
        print(f"Directory error: {os_error}")
    except Exception as e:
        print(f"Unexpected error: {e}")

asyncio.run(main())
