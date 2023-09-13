## Usage: python3 docgen.py output.json
## change the output.json to a different file if running this in parallel

import random
import json, sys
from nltk.corpus import reuters 
from faker import Faker
import nltk
nltk.download('reuters')
from sentence_transformers import SentenceTransformer

# Load the pre-trained SentenceTransformer model
model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
file=sys.argv[1]

# Initialize the Faker instance
fake = Faker()

# Number of documents to generate
num_documents = 350000
num_sentences_per_document = 10

# generate dummy documents
with open(file, "w") as json_file:
    for _ in range(num_documents):
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

#payload for the Elasticsearch Bulk API
        payload = ""
        payload += json.dumps({"index": {"_index": "document"}}) + "\n"
        payload += json.dumps(document) + "\n"  
        json_file.write(payload)
