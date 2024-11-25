import asyncio
import os
import json

from utils.gemini import scan_txt
from utils.parse_json import parse_json


async def main():
    source_dir = "storage/results"

    # Iterate through files in the folder
    for index, dir in enumerate(os.listdir(source_dir)):
        key = index % 4 + 1

        source_folder = os.path.join(source_dir, dir)
        file_path = os.path.join(source_folder, 'full_text.txt')

        print("AI parsing:", dir)
        print("Number:", index + 1, "\n")

        scan_text = scan_txt(file_path, key)
        try:
            result = parse_json(scan_text)

            if result is not None:
                json_path = os.path.join(source_folder, 'gemini.json')
                # Save result to a JSON file
                with open(json_path, "w") as f:
                    json.dump(result, f)
            else:
                print("Parsing result is None.")
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"An error occurred while processing: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        if key == 4:
            await asyncio.sleep(10)


asyncio.run(main())