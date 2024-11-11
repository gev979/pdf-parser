import asyncio

from flair.data import Corpus
from flair.datasets import ColumnCorpus
from flair.models import SequenceTagger
from flair.trainers import ModelTrainer
from flair.embeddings import WordEmbeddings, StackedEmbeddings


async def main():
    # define columns
    columns = {0: 'text', 1: 'ner'}

    # this is the folder in which train, test and dev files reside
    data_folder = 'resources/train'

    # init a corpus using column format, data folder and the names of the train, dev and test files
    corpus: Corpus = ColumnCorpus(data_folder, columns,
                                train_file='train.txt',
                                test_file='test.txt',
                                dev_file='dev.txt')
                            
    # Define embeddings
    embeddings = StackedEmbeddings([WordEmbeddings('glove')])

    # Initialize sequence tagger with desired tag type (e.g., 'ner')
    tagger = SequenceTagger(hidden_size=256,
                            embeddings=embeddings,
                            tag_dictionary=corpus.make_tag_dictionary(tag_type='ner'),
                            tag_type='ner')

    # Initialize trainer
    trainer = ModelTrainer(tagger, corpus)

    # Start training
    trainer.train('resources/taggers/ner',
                learning_rate=0.1,
                mini_batch_size=32,
                max_epochs=10)

asyncio.run(main())