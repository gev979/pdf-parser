import asyncio
import os
import io
import sys
import re
import shutil
import json

from utils.gemini import scan_txt

async def main():
    source_dir = "storage/results_v1"
    directory = "storage/results_v2"
    os.makedirs(directory, exist_ok=True)

    # Iterate through files in the folder
    for dir in os.listdir(source_dir):
        source_folder = os.path.join(source_dir, dir)
        destination_folder = os.path.join(directory, dir)

        for item in os.listdir(source_folder):
            if item not in ['images', 'file.pdf', 'full_text.txt']:
                continue

            source_path = os.path.join(source_folder, item)
            destination_path = os.path.join(destination_folder, item)
            
            if os.path.isdir(source_path):
                # Copy entire folder
                shutil.copytree(source_path, destination_path, dirs_exist_ok=True)
            else:
                # Copy individual file
                shutil.copy2(source_path, destination_path)

        file_path = os.path.join(destination_folder, 'full_text.txt')

        result = scan_txt(file_path)
        print(result)
        if result is not None:
            json_path = os.path.join(destination_folder, 'output.json')
            # Save out_meta to a JSON file
            with open(json_path, "w") as f:
                json.dump(json.loads(result), f)
        
        break

asyncio.run(main())