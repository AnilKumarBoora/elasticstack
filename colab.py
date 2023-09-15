from google.colab import drive
drive.mount('/content/drive')

!pip3 install faker nltk sentence_transformers

import random
import json, sys
from nltk.corpus import reuters
from faker import Faker
import nltk
nltk.download('reuters')
nltk.download('punkt')
from sentence_transformers import SentenceTransformer

def get_document():
    content = " ".join([" ".join(reuters.sents(categories=random.choice(reuters.categories()))[0]) for _ in range(num_sentences_per_document)])

    document = {
        '_split_id': random.randint(1, 1000),
        'character': random.choice(['A', 'B', 'C', 'D']),
        'content': content,
        'content_type': random.choice(['news', 'article']),
        'name': fake.sentence()[:50],
        'permalink': f'https://example.com/{random.randint(1000, 9999)}',
        'source_title': fake.sentence()[:50],
        'embedding': model.encode(content).tolist(),
    }

    return document

model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
file="payload00.json"

# Initialize the Faker instance
fake = Faker()

# Number of documents to generate
num_documents = 350000
num_sentences_per_document = 10

count = 0
file = "/content/drive/MyDrive/payload21.json"
with open(file, "w") as json_file:
    for _ in range(num_documents):
        content = " ".join([" ".join(reuters.sents(categories=random.choice(reuters.categories()))[0]) for _ in range(num_sentences_per_document)])

        document = get_document()

#payload for the Elasticsearch Bulk API
        payload = ""
        payload += json.dumps({"index": {"_index": "document"}}) + "\n"
        payload += json.dumps(document) + "\n"
        json_file.write(payload)
        count = count + 1
        if count % 1000 == 0:
            print(count)