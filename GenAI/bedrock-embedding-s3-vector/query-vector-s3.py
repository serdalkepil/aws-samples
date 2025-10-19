# Query a vector index with an embedding from Amazon Titan Text Embeddings V2.
import boto3 
import json 

# Create Bedrock Runtime and S3 Vectors clients in the AWS Region of your choice. 
bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")
s3vectors = boto3.client("s3vectors", region_name="us-east-1") 

# Query text to convert to an embedding. 
input_text = "adventures in space"

# Generate the vector embedding.
response = bedrock.invoke_model(
    modelId="amazon.titan-embed-text-v2:0",
    body=json.dumps({"inputText": input_text})
) 

# Extract embedding from response.
model_response = json.loads(response["body"].read())
embedding = model_response["embedding"]

print(json.dumps(embedding, indent=2))

print("Querying vector index...\n")

# Query vector index.
response = s3vectors.query_vectors(
    vectorBucketName="ozu-vector-bucket",
    indexName="movies",
    queryVector={"float32": embedding}, 
    topK=3, 
    returnDistance=True,
    returnMetadata=True
)
print(json.dumps(response["vectors"], indent=2))

print("Querying vector index with a metadata filter...\n")

# Query vector index with a metadata filter.
response = s3vectors.query_vectors(
    vectorBucketName="ozu-vector-bucket",
    indexName="movies",
    queryVector={"float32": embedding}, 
    topK=3, 
    filter={"genre": "scifi"},
    returnDistance=True,
    returnMetadata=True
)
print(json.dumps(response["vectors"], indent=2))
