import os
import json
import re
import shutil


def convert_to_uppercase_with_underscores(word):
    return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', word).upper()

def convert_to_iob(key, text, label):
    formatted_words = []

    if not isinstance(label, str):
        return formatted_words

    if isinstance(key, str):
        key_words = key.split()
        for i, word in enumerate(key_words):
            if i == 0:
                formatted_words.append(f"{word} B-{convert_to_uppercase_with_underscores(label)}-K")
            else:
                formatted_words.append(f"{word} I-{convert_to_uppercase_with_underscores(label)}-K")

    if isinstance(text, str):
        text_words = text.split()
        for i, word in enumerate(text_words):
            if i == 0:
                formatted_words.append(f"{word} B-{convert_to_uppercase_with_underscores(label)}-V")
            else:
                formatted_words.append(f"{word} I-{convert_to_uppercase_with_underscores(label)}-V")

    return formatted_words


def delete_existing_chunks(output_dir):
    """Deletes the chunks folder if it exists"""
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
        print(f"Deleted existing folder: {output_dir}")
    else:
        print(f"No existing folder to delete: {output_dir}")


def split_file(input_file, output_dir, chunk_size=10000, dev_fraction=0.10, test_fraction=0.05):
    # Read the input train file
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # Calculate the number of chunks
    num_chunks = len(lines) // chunk_size + (1 if len(lines) % chunk_size != 0 else 0)

    for i in range(num_chunks):
        # Get the lines for this chunk
        chunk_lines = lines[i * chunk_size:(i + 1) * chunk_size]

        # Create folder for this chunk
        chunk_folder = os.path.join(output_dir, f"train_{i + 1}")
        os.makedirs(chunk_folder, exist_ok=True)

        # Define file paths for train, dev, and small parts files
        train_file_path = os.path.join(chunk_folder, 'train.txt')
        dev_file_path = os.path.join(chunk_folder, 'dev.txt')
        test_file_path = os.path.join(chunk_folder, 'test.txt')

        # Calculate the number of lines for dev and small part (fractions of the chunk)
        dev_size = int(len(chunk_lines) * dev_fraction)
        test_size = int(len(chunk_lines) * test_fraction)

        # Split the chunk into main train, dev, and small part files
        dev_lines = chunk_lines[:dev_size]
        test_lines = chunk_lines[dev_size:dev_size + test_size]
        train_lines = chunk_lines[dev_size + test_size:]

        # Write the train, dev, and small part files
        with open(train_file_path, 'w') as train_file:
            train_file.writelines(train_lines)

        with open(dev_file_path, 'w') as dev_file:
            dev_file.writelines(dev_lines)

        with open(test_file_path, 'w') as test_file:
            test_file.writelines(test_lines)

        print(f"Created chunk {i + 1}: {train_file_path}, {dev_file_path}, {test_file_path}")


def main():
    directory = 'storage/results'

    dirs = os.listdir(directory)
    # dirs_length = 50
    dirs_length = len(dirs)

    train_dir = 'resources/train'
    paths = [
        os.path.join(train_dir, 'train.txt'),
        os.path.join(train_dir, 'dev.txt'),
        os.path.join(train_dir, 'test.txt')
    ]

    # Create the directory if it doesn't exist
    if not os.path.exists(train_dir):
        os.makedirs(train_dir)

    # Create the files if they don't exist
    for path in paths:
        with open(path, 'w') as file:
            pass

    base_path = paths[0]

    for i, dirc in enumerate(dirs):
        if i > dirs_length:
            break

        json_path = os.path.join(directory, dirc, 'gemini.json')

        if not os.path.exists(json_path):
            continue

        with open(json_path, 'r') as file:
            json_data = json.load(file)

        # if dirs_length - 10 > i > dirs_length - 30:
        if dirs_length - 500 > i > dirs_length - 1000:
            with open(paths[1], "a") as file:
                for entry in json_data["meta"]:
                    label = entry.get("label", None)
                    text = entry.get("text", None)
                    key = entry.get("key", None)

                    formatted_text = convert_to_iob(key, text, label)
                    for line in formatted_text:
                        file.write(line + "\n")

                    file.write("\n")

        # elif i >= dirs_length - 40:
        elif i >= dirs_length - 300:
            with open(paths[2], "a") as file:
                for entry in json_data["meta"]:
                    label = entry.get("label", None)
                    text = entry.get("text", None)
                    key = entry.get("key", None)

                    formatted_text = convert_to_iob(key, text, label)
                    for line in formatted_text:
                        file.write(line + "\n")

                    file.write("\n")

        with open(base_path, "a") as file:
            for entry in json_data["meta"]:
                label = entry.get("label", None)
                text = entry.get("text", None)
                key = entry.get("key", None)

                formatted_text = convert_to_iob(key, text, label)
                for line in formatted_text:
                    file.write(line + "\n")

                file.write("\n")

    # Specify input and output paths
    input_file = 'resources/train/train.txt'  # Your original train.txt file
    output_dir = 'resources/train/chunks'  # Directory where chunks will be saved

    # Delete existing chunks folder if it exists
    delete_existing_chunks(output_dir)

    # Split the file and create folders for each chunk
    # split_file(input_file, output_dir, chunk_size = 1000)


main()