import pytesseract
import io
import os
import json
from PIL import Image
from marker.convert import convert_single_pdf
from marker.models import load_all_models
from utils.file import upload

RESULT_DIRECTORY = "storage/results_v1"

# Ensure the PDF and result directories exist
os.makedirs(RESULT_DIRECTORY, exist_ok=True)

async def parse_with_pdf_marker(file):
    file_location, unique_folder_name = await upload(file, RESULT_DIRECTORY)

    # Call the PDF conversion function
    fpath = file_location
    model_lst = load_all_models()
    full_text, images, out_meta = convert_single_pdf(fpath, model_lst)

    # Create a unique folder for this PDF's results without the file extension
    pdf_result_folder = os.path.join(RESULT_DIRECTORY, unique_folder_name)
    os.makedirs(pdf_result_folder, exist_ok=True)

    # Define paths for saving text, metadata, and images
    text_file = os.path.join(pdf_result_folder, "full_text.txt")
    meta_file = os.path.join(pdf_result_folder, "out_meta.json")
    images_folder = os.path.join(pdf_result_folder, "images")
    os.makedirs(images_folder, exist_ok=True)

    # Save full_text to a text file
    with open(text_file, "w") as f:
        f.write(full_text)

    # Save each image and store the path
    image_paths = []
    for filename, image in images.items():
        image_path = os.path.join(images_folder, filename)
        image.save(image_path, "PNG")
        image_paths.append(image_path)

    # Save out_meta to a JSON file
    with open(meta_file, "w") as f:
        json.dump(out_meta, f)

    # Return paths to saved files
    return {
        "text_file": text_file,
        "images_folder": images_folder,
        "meta_file": meta_file,
    }
