from elasticsearch import Elasticsearch
import time
import numpy as np
import json, sys, random
from nltk.corpus import reuters
from faker import Faker
import nltk
nltk.download('reuters')
from sentence_transformers import SentenceTransformer

# Load the pre-trained SentenceTransformer model
model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')

# Initialize the Faker instance
fake = Faker()

# Number of documents to generate
num_sentences_per_document = 10



# Elasticsearch authentication credentials
username = "elastic"
password = "JVPfhFPSNmLGpk-Rwjm0"

# Initialize Elasticsearch client with authentication
es = Elasticsearch(
    "https://localhost:9200",
    basic_auth=(username, password),
    ca_certs="/home/mammonplus/eland/ca/ca.crt"
)

# Number of requests
num_requests = 50

# List to store the time taken for each request
request_times = []

for _ in range(num_requests):
    content = " ".join([" ".join(reuters.sents(categories=random.choice(reuters.categories()))[0]) for _ in range(num_sentences_per_document)])
    print(content)
    start = random.randint(1, 900)
    end = start + random.randint(10, 300)

    # only vector search
    vector_query = {
            "knn": {
                "field": "embedding",
                "query_vector": model.encode(content).tolist(),
                "k": 10,
                "num_candidates": 100
        },
        "_source": ["_split_id", "content"]
    }

    #  vector plus meta data search
    vector_meta_query = {
            "knn": {
                "field": "embedding",
                "query_vector": model.encode(content).tolist(),
                "k": 10,
                "num_candidates": 100,
                "filter": {
                    "range": {
                        "_split_id": {
                            "gte": start,
                            "lte": end
                        }
                    }
                }
        },
        "_source": ["_split_id", "content"]
    }

    # use either vector_meta_query or vector_query
    es_query = vector_meta_query
    
    start_time = time.time()

    # Make your Elasticsearch request here
    # For example, let's say you are searching for a document with a specific query
    response = es.search(index='document', body=es_query)

    end_time = time.time()
    took = response.get('took', 0)  # Get the 'took' attribute from the Elasticsearch response
    print(took)
    request_times.append(took)  # milliseconds

# Calculate statistics
mean_time = np.mean(request_times)
percentile_80 = np.percentile(request_times, 80)
percentile_90 = np.percentile(request_times, 90)
max_time = np.max(request_times)
min_time = np.min(request_times)

# Display the statistics
print(f"Number of Requests: {num_requests}")
print(f"Mean Time: {mean_time:.6f} milliseconds")
print(f"80th Percentile: {percentile_80:.6f} milliseconds")
print(f"90th Percentile: {percentile_90:.6f} milliseconds")
print(f"Max Time: {max_time:.6f} milliseconds")
print(f"Min Time: {min_time:.6f} milliseconds")