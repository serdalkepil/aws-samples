# Vectors and Vector Databases - Complete Guide

## 1. What are Vectors?

### Mathematical Definition
A vector is a mathematical object that has both **magnitude** and **direction**. In computing, we typically work with numerical vectors as arrays of numbers.

```python
# Example vectors in different dimensions
vector_2d = [3, 4]           # 2-dimensional vector
vector_3d = [1, 2, 3]        # 3-dimensional vector 
vector_high_dim = [0.1, 0.5, -0.3, 0.8, ...]  # High-dimensional vector (e.g., 384 dimensions)
```

### Vectors in AI/ML Context
In artificial intelligence, vectors are used to represent data in numerical form:

```python
# Text converted to vector
text = "machine learning"
vector_representation = [0.23, -0.45, 0.67, 0.12, -0.89, ...]  # 384+ dimensions

# Image converted to vector
image_pixels = "image data"
vector_representation = [0.56, 0.78, -0.34, 0.91, ...]  # High-dimensional vector
```

## 2. How Data Becomes Vectors

### Embedding Process
```python
# Example: Converting text to vectors using embedding models
from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Convert text to vector
sentences = ["machine learning", "artificial intelligence", "deep learning"]
embeddings = model.encode(sentences)

print(f"Text: {sentences[0]}")
print(f"Vector shape: {embeddings[0].shape}")  # (384,) - 384-dimensional vector
print(f"Sample vector: {embeddings[0][:5]}")   # First 5 dimensions
```

### Different Types of Embeddings
- **Text Embeddings**: Convert words/sentences to vectors
- **Image Embeddings**: Convert images to vectors
- **Audio Embeddings**: Convert sound to vectors
- **Graph Embeddings**: Convert network data to vectors

## 3. Vector Similarity and Distance

### Why Similarity Matters
Vectors that are "close" in vector space represent similar content.

```python
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Example vectors
vector_cat = [0.8, 0.6, 0.1, 0.2]      # Represents "cat"
vector_dog = [0.7, 0.5, 0.2, 0.3]      # Represents "dog" 
vector_car = [0.1, 0.2, 0.9, 0.8]      # Represents "car"

# Calculate similarity
similarity_pet = cosine_similarity([vector_cat], [vector_dog])[0][0]    # High similarity
similarity_pet_car = cosine_similarity([vector_cat], [vector_car])[0][0] # Low similarity

print(f"Cat-Dog similarity: {similarity_pet:.3f}")      # ~0.98
print(f"Cat-Car similarity: {similarity_pet_car:.3f}")  # ~0.35
```

### Distance Metrics
```python
def euclidean_distance(vec1, vec2):
    return np.sqrt(np.sum((np.array(vec1) - np.array(vec2)) ** 2))

def cosine_similarity_custom(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    return dot_product / (norm1 * norm2)

# Example usage
vec1 = [1, 2, 3]
vec2 = [4, 5, 6]

print(f"Euclidean distance: {euclidean_distance(vec1, vec2):.3f}")
print(f"Cosine similarity: {cosine_similarity_custom(vec1, vec2):.3f}")
```

## 4. What are Vector Databases?

### Definition
A **vector database** is a specialized database designed to store, index, and query high-dimensional vectors efficiently.

### Traditional DB vs Vector DB
```python
# Traditional Database Query
"""
SELECT * FROM products 
WHERE category = 'electronics' 
AND price < 1000;
"""

# Vector Database Query  
"""
FIND vectors SIMILAR TO [0.23, -0.45, 0.67, ...]
WHERE similarity > 0.8
LIMIT 10;
"""
```

## 5. How Vector Databases Work

### Core Components
```python
# Simplified vector database architecture
class SimpleVectorDB:
    def __init__(self):
        self.vectors = []      # Store vectors
        self.metadata = []     # Store associated data
        self.index = None      # For fast searching
    
    def add_vector(self, vector, metadata):
        self.vectors.append(vector)
        self.metadata.append(metadata)
    
    def search_similar(self, query_vector, top_k=5):
        similarities = []
        for i, vector in enumerate(self.vectors):
            similarity = cosine_similarity_custom(query_vector, vector)
            similarities.append((similarity, i))
        
        # Sort by similarity and return top K
        similarities.sort(reverse=True)
        return [(self.metadata[i], sim) for sim, i in similarities[:top_k]]
```

### Real Vector Database Operations
```python
# Using Pinecone (popular vector DB) as example
import pinecone

# Initialize
pinecone.init(api_key="your-api-key", environment="us-west1-gcp")

# Create index
pinecone.create_index("documents", dimension=384, metric="cosine")

# Connect to index
index = pinecone.Index("documents")

# Store vectors
vectors = [
    ("vec1", [0.1, 0.2, 0.3, ...], {"text": "machine learning tutorial", "category": "education"}),
    ("vec2", [0.4, 0.5, 0.6, ...], {"text": "AI research paper", "category": "research"})
]
index.upsert(vectors=vectors)

# Search similar vectors
query_vector = [0.15, 0.25, 0.35, ...]  # From user query
results = index.query(vector=query_vector, top_k=5, include_metadata=True)
```

## 6. Popular Vector Databases

### Commercial Solutions
- **Pinecone**: Fully managed, easy to use
- **Weaviate**: Open-source with GraphQL interface
- **Chroma**: Lightweight, open-source
- **Qdrant**: High-performance, open-source
- **Milvus**: Scalable, for large-scale applications

### AWS Vector Database Options
```python
# Amazon Bedrock with Vector Databases
"""
AWS offers several options:
1. Amazon Aurora PostgreSQL with pgvector extension
2. Amazon OpenSearch with k-NN plugin  
3. Amazon Neptune with vector capabilities
4. Partner solutions (Pinecone, Weaviate) on AWS Marketplace
"""
```

## 7. Complete RAG Example with Vectors

### Retrieval-Augmented Generation Pipeline
```python
import boto3
import numpy as np
from sentence_transformers import SentenceTransformer

class RAGSystem:
    def __init__(self):
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.vector_db = self.initialize_vector_db()
        self.bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
    
    def initialize_vector_db(self):
        # Simplified in-memory DB for demo
        return SimpleVectorDB()
    
    def add_documents(self, documents):
        """Add documents to vector database"""
        for doc in documents:
            # Convert text to vector
            vector = self.embedder.encode(doc['content'])
            # Store in vector DB
            self.vector_db.add_vector(vector, doc)
    
    def search_documents(self, query, top_k=3):
        """Search for similar documents"""
        query_vector = self.embedder.encode(query)
        results = self.vector_db.search_similar(query_vector, top_k=top_k)
        return results
    
    def generate_response(self, query, context_documents):
        """Generate response using Bedrock with context"""
        context = "\n\n".join([doc['content'] for doc, _ in context_documents])
        
        prompt = f"""
        Human: Based on the following context, please answer the question.

        Context:
        {context}

        Question: {query}

        Please provide a comprehensive answer based only on the provided context.

        Assistant:
        """
        
        response = self.bedrock.invoke_model(
            modelId='anthropic.claude-v2',
            body=json.dumps({
                "prompt": prompt,
                "max_tokens_to_sample": 500,
                "temperature": 0.1
            })
        )
        
        return json.loads(response['body'].read())['completion']

# Usage Example
def demo_rag_system():
    # Initialize RAG system
    rag = RAGSystem()
    
    # Add some documents
    documents = [
        {
            'id': 1,
            'content': 'Machine learning is a subset of artificial intelligence that enables computers to learn without being explicitly programmed.',
            'source': 'AI Textbook'
        },
        {
            'id': 2, 
            'content': 'Deep learning uses neural networks with multiple layers to learn complex patterns in large amounts of data.',
            'source': 'Research Paper'
        },
        {
            'id': 3,
            'content': 'Vector databases store data as high-dimensional vectors and enable semantic search based on similarity.',
            'source': 'Tech Blog'
        }
    ]
    
    rag.add_documents(documents)
    
    # Search and generate
    query = "What is machine learning?"
    similar_docs = rag.search_documents(query, top_k=2)
    response = rag.generate_response(query, similar_docs)
    
    print(f"Query: {query}")
    print(f"Found {len(similar_docs)} relevant documents")
    print(f"Generated response: {response}")

# Run the demo
demo_rag_system()
```

## 8. Real-World Applications

### Use Cases
```python
# 1. Semantic Search
"""
Traditional: "Find documents containing 'AI'"
Vector-based: "Find documents about artificial intelligence and machine learning"
"""

# 2. Recommendation Systems
"""
User vector: [0.8, 0.6, 0.3, ...] (represents user preferences)
Find similar product vectors
"""

# 3. Anomaly Detection
"""
Normal behavior vectors vs anomaly vectors
Detect outliers in high-dimensional space
"""

# 4. Image/Video Search
"""
Query: "Find images similar to this sunset photo"
Convert images to vectors and search
"""

# 5. Chatbots and QA Systems
"""
Retrieve relevant information before generating responses
(RAG - Retrieval Augmented Generation)
"""
```

## 9. Key Benefits of Vector Databases

### Advantages
1. **Semantic Understanding**: Finds conceptually similar content
2. **High Performance**: Optimized for similarity searches
3. **Scalability**: Handles millions of high-dimensional vectors
4. **Flexibility**: Works with any type of data (text, images, audio)
5. **Real-time Search**: Fast query responses

### When to Use Vector Databases
- ✅ Semantic search applications
- ✅ Recommendation systems  
- ✅ Similarity matching
- ✅ Anomaly detection
- ✅ RAG applications
- ❌ Simple key-value lookups
- ❌ Transactional applications
- ❌ Structured data with exact matches

## 10. Getting Started

### Simple Implementation
```python
# Basic vector similarity search
def simple_vector_search(query_embedding, document_embeddings, documents, top_k=5):
    similarities = []
    
    for i, doc_embedding in enumerate(document_embeddings):
        similarity = cosine_similarity_custom(query_embedding, doc_embedding)
        similarities.append((similarity, documents[i]))
    
    # Sort by similarity (highest first)
    similarities.sort(key=lambda x: x[0], reverse=True)
    return similarities[:top_k]

# Example usage
documents = ["machine learning", "artificial intelligence", "data science", "computer vision"]
document_embeddings = [model.encode(doc) for doc in documents]

query = "AI technology"
query_embedding = model.encode(query)

results = simple_vector_search(query_embedding, document_embeddings, documents)
for similarity, doc in results:
    print(f"Similarity: {similarity:.3f} - Document: {doc}")
```

This comprehensive guide shows how vectors transform unstructured data into numerical representations that computers can understand and compare, while vector databases provide the infrastructure to efficiently store and query these representations for powerful AI applications.