import torch
torch.cuda.empty_cache()

from flair.embeddings import WordEmbeddings, FlairEmbeddings, StackedEmbeddings
from flair.models import SequenceTagger
from flair.trainers import ModelTrainer
from corpus_initializer import corpus


# 2. what label do we want to predict?
label_type = 'ner'

# 3. make the label dictionary from the corpus
label_dict = corpus.make_label_dictionary(label_type=label_type, add_unk=False)

# 4. initialize embedding stack with Flair and GloVe
embedding_types = [
    WordEmbeddings('glove'),
    FlairEmbeddings('news-forward'),
    FlairEmbeddings('news-backward'),
]

embeddings = StackedEmbeddings(embeddings=embedding_types)

# 5. initialize sequence tagger
tagger = SequenceTagger(hidden_size=256,
                        embeddings=embeddings,
                        tag_dictionary=label_dict,
                        tag_type=label_type)

# 6. initialize trainer
trainer = ModelTrainer(tagger, corpus)

# 7. run fine-tuning
trainer.train('resources/taggers/ner',
              learning_rate=0.1,
              mini_batch_size=4,
              max_epochs=150)
