import os
import json
import re

def convert_to_uppercase_with_underscores(word):
    return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', word).upper()

def convert_to_iob(key, text, label):
    formatted_words = []

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
        train_dir + '/train.txt', 
        train_dir + '/dev.txt', 
        train_dir + '/test.txt'
    ]
    for file_path in paths:
        with open(file_path, 'w') as file:
            pass    

    for i, dir in enumerate(dirs):
        json_path = os.path.join(directory, dir, 'output.json')
        
        if i < dirs_length - 10:
            path = paths[0]
        elif i < dirs_length - 3:
            path = paths[1]
        else:
            path = paths[2]

        with open(json_path, 'r') as file:
            json_data = json.load(file)
        
        with open(path, "a") as file:
            for entry in json_data["meta"]:
                label = entry.get("label", None)
                text = entry.get("text", None)
                key = entry.get("key", None)

                formatted_text = convert_to_iob(key, text, label)
                for line in formatted_text:
                    file.write(line + "\n")

                file.write("\n")


main()