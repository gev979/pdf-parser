import json
import os

from flair.models import SequenceTagger
from flair.data import Sentence
from flair.splitter import SegtokSentenceSplitter

# Load the Flair model for NER (adjust the path as needed)
tagger = SequenceTagger.load("resources/taggers/ner/final-model.pt")

def main():
    directory = 'storage/results_v2'
    dirs = os.listdir(directory)

    for dir in dirs:
        full_dir = os.path.join(directory, dir)
        text_file_path = os.path.join(full_dir, 'full_text.txt')

        # Read the entire content of the file
        with open(text_file_path, 'r') as file:
            full_text = file.read()

        # full_text = "George Washington went to Washington"

        # Initialize sentence splitter
        splitter = SegtokSentenceSplitter()
        
        # Split text into list of sentences
        sentences = splitter.split(full_text)
        
        # Predict NER tags for each sentence
        tagger.predict(sentences)

        # Extract labels and their tags
        labels = []
        for sentence in sentences:
            for label in sentence.get_labels():
                labels.append({
                    "text": label.data_point.text,
                    "label": label.value,
                    "score": label.score
                })

        # Save labels to a JSON file
        labels_file = os.path.join(full_dir, 'labels.json')
        with open(labels_file, "w") as f:
            json.dump(labels, f)

main()