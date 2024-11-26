from flair.data import Corpus
from flair.datasets import ColumnCorpus

# Define column mapping
columns = {0: 'text', 1: 'ner'}

# Folder containing train, test, and dev files
data_folder = 'resources/train'

# Initialize corpus
corpus: Corpus = ColumnCorpus(
    data_folder,
    columns,
    train_file='train.txt',
    test_file='test.txt',
    dev_file='dev.txt'
)
