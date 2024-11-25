import os
import json
import re

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

def main():
    directory = 'storage/results_v2'

    dirs = os.listdir(directory)
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

    for i, dir in enumerate(dirs):
        json_path = os.path.join(directory, dir, 'output.json')

        with open(json_path, 'r') as file:
            json_data = json.load(file)

        if i < dirs_length - 5 and i > dirs_length - 10:
            with open(paths[1], "a") as file:
                for entry in json_data["meta"]:
                    label = entry.get("label", None)
                    text = entry.get("text", None)
                    key = entry.get("key", None)

                    formatted_text = convert_to_iob(key, text, label)
                    for line in formatted_text:
                        file.write(line + "\n")

                    file.write("\n")

        elif i >= dirs_length - 3:
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


main()