import re
import os
import google.generativeai as genai

api_key = os.environ['GEMINI_API_KEY']
genai.configure(api_key=api_key)

# Create the model
generation_config = {
  "temperature": 1,
  "max_output_tokens": 8192,
  "response_mime_type": "application/json",
}

# Open the file in read mode
with open('system_instruction.txt', 'r') as file:
    # Read the contents of the file
    system_instruction = file.read()

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  system_instruction=system_instruction
)

def scan_txt(file_path):
    # Read and process the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Minify the content by removing empty lines, extra spaces, and ensuring readability
    minified_content = []
    for line in lines:
        # Strip leading/trailing whitespaces
        stripped_line = line.strip()

        if stripped_line:  # If line is not empty
            # Replace multiple spaces with a single space
            stripped_line = re.sub(r'\s+', ' ', stripped_line)

            # Add the processed line to the minified content list
            minified_content.append(stripped_line)

    # Join the lines back together, ensuring at least a single space between sentences
    final_content = ' '.join(minified_content)

    # Optionally, ensure proper punctuation (you may tweak this depending on your needs)
    final_content = re.sub(r'(\.|\!|\?)(?=\S)', r'\1 ', final_content)

    try:
        response = model.generate_content(final_content)
        return response.text
    except Exception as e:
        print(f"Error: {e}")
        return None  