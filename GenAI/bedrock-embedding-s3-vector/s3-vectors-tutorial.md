# Amazon S3 Vectors Getting Started Tutorial

This tutorial shows how to use Amazon S3 Vectors to store and query vector embeddings for semantic search applications.

## Prerequisites

- AWS CLI configured
- Python 3.x with boto3
- S3 bucket with vector indexing enabled

## Step 1: Create Vector Index

```bash
# Create S3 bucket with vector indexing
aws s3api create-bucket --bucket your-vector-bucket --region us-east-1

# Enable vector indexing on the bucket
aws s3api put-bucket-vector-configuration \
    --bucket your-vector-bucket \
    --vector-configuration Status=Enabled
```

## Step 2: Generate and Store Embeddings

```python
import boto3
import json

# Initialize clients
bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")
s3vectors = boto3.client("s3vectors", region_name="us-east-1")

# Sample texts
texts = [
    "Star Wars: A farm boy joins rebels to fight an evil empire in space",
    "Jurassic Park: Scientists create dinosaurs in a theme park that goes wrong",
    "Finding Nemo: A father fish searches the ocean to find his lost son"
]

# Generate embeddings
embeddings = []
for text in texts:
    response = bedrock.invoke_model(
        modelId="amazon.titan-embed-text-v2:0",
        body=json.dumps({"inputText": text})
    )
    response_body = json.loads(response["body"].read())
    embeddings.append(response_body["embedding"])

# Store vectors with metadata
s3vectors.put_vectors(
    vectorBucketName="your-vector-bucket",
    indexName="movies",
    vectors=[
        {
            "key": "star-wars",
            "data": {"float32": embeddings[0]},
            "metadata": {"title": "Star Wars", "genre": "scifi"}
        },
        {
            "key": "jurassic-park", 
            "data": {"float32": embeddings[1]},
            "metadata": {"title": "Jurassic Park", "genre": "scifi"}
        },
        {
            "key": "finding-nemo",
            "data": {"float32": embeddings[2]},
            "metadata": {"title": "Finding Nemo", "genre": "family"}
        }
    ]
)
```

## Step 3: Query Vectors

```python
# Query with text
query_text = "space adventure movie"

# Generate query embedding
query_response = bedrock.invoke_model(
    modelId="amazon.titan-embed-text-v2:0",
    body=json.dumps({"inputText": query_text})
)
query_embedding = json.loads(query_response["body"].read())["embedding"]

# Search similar vectors
search_response = s3vectors.query_vectors(
    vectorBucketName="your-vector-bucket",
    indexName="movies",
    queryVector={"float32": query_embedding},
    maxResults=3
)

# Display results
for result in search_response["matches"]:
    print(f"Movie: {result['metadata']['title']}")
    print(f"Score: {result['score']}")
    print(f"Genre: {result['metadata']['genre']}")
    print("---")
```

## Step 4: Filter by Metadata

```python
# Search with metadata filter
filtered_response = s3vectors.query_vectors(
    vectorBucketName="your-vector-bucket",
    indexName="movies",
    queryVector={"float32": query_embedding},
    metadataFilter={
        "genre": {"stringEquals": "scifi"}
    },
    maxResults=5
)
```

## Complete Example

```python
import boto3
import json

def setup_s3_vectors():
    """Complete S3 Vectors example"""
    
    # Initialize clients
    bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")
    s3vectors = boto3.client("s3vectors", region_name="us-east-1")
    
    bucket_name = "your-vector-bucket"
    index_name = "movies"
    
    # 1. Store vectors
    texts = ["Space adventure", "Dinosaur theme park", "Ocean fish story"]
    
    embeddings = []
    for text in texts:
        response = bedrock.invoke_model(
            modelId="amazon.titan-embed-text-v2:0",
            body=json.dumps({"inputText": text})
        )
        embeddings.append(json.loads(response["body"].read())["embedding"])
    
    s3vectors.put_vectors(
        vectorBucketName=bucket_name,
        indexName=index_name,
        vectors=[
            {"key": f"movie-{i}", "data": {"float32": emb}, "metadata": {"text": text}}
            for i, (emb, text) in enumerate(zip(embeddings, texts))
        ]
    )
    
    # 2. Query vectors
    query_response = bedrock.invoke_model(
        modelId="amazon.titan-embed-text-v2:0",
        body=json.dumps({"inputText": "space movie"})
    )
    query_embedding = json.loads(query_response["body"].read())["embedding"]
    
    results = s3vectors.query_vectors(
        vectorBucketName=bucket_name,
        indexName=index_name,
        queryVector={"float32": query_embedding},
        maxResults=3
    )
    
    return results["matches"]

if __name__ == "__main__":
    matches = setup_s3_vectors()
    for match in matches:
        print(f"Text: {match['metadata']['text']}, Score: {match['score']}")
```

## Key Features

- **Serverless**: No infrastructure to manage
- **Scalable**: Handles billions of vectors
- **Integrated**: Works with Bedrock embeddings
- **Metadata filtering**: Rich query capabilities
- **Cost-effective**: Pay per query

## Use Cases

- Semantic search
- Recommendation systems
- RAG (Retrieval Augmented Generation)
- Content similarity
- Document clustering

## Best Practices

1. Use consistent embedding models
2. Include relevant metadata
3. Batch vector operations
4. Monitor query performance
5. Use appropriate vector dimensions