## 1. Basic Text Prompt Structure

### Simple Completion Prompt
```python
basic_prompt = """
Human: Write a short description of artificial intelligence.

Assistant:
"""
```

### Chat-style Prompt
```python
chat_prompt = """
Human: Hello! Can you help me understand how machine learning works?

Assistant: Of course! I'd be happy to explain machine learning in simple terms.
"""
```

## 2. Parameter Tuning Examples

### Temperature Control (Creativity)
```python
# Low temperature (more deterministic)
low_temp_prompt = {
    "prompt": "Human: List the main benefits of cloud computing.\n\nAssistant:",
    "temperature": 0.2,
    "max_tokens": 200
}

# High temperature (more creative)
high_temp_prompt = {
    "prompt": "Human: Write a creative story about a robot learning to paint.\n\nAssistant:",
    "temperature": 0.8,
    "max_tokens": 300
}
```

### Token Limits
```python
# Short response
short_response = {
    "prompt": "Human: What is Python?\n\nAssistant:",
    "max_tokens": 50
}

# Long response
long_response = {
    "prompt": "Human: Explain the complete software development lifecycle in detail.\n\nAssistant:",
    "max_tokens": 500
}
```

## 3. Context and Instruction Tuning

### Adding Context
```python
context_prompt = """
Human: You are an expert software architect. Explain microservices architecture to a beginner.

Context: The person asking is a junior developer familiar with monolithic applications but new to distributed systems.

Question: What are the key advantages of microservices over monoliths?

Assistant:
"""
```

### Step-by-Step Instructions
```python
instruction_prompt = """
Human: Please follow these instructions carefully:
1. Analyze the given code snippet
2. Identify any potential bugs
3. Suggest improvements
4. Provide the corrected code

Code:
def calculate_average(numbers):
    return sum(numbers) / len(numbers)

What issues do you see with this function?

Assistant:
"""
```

## 4. Few-Shot Learning Examples

### Classification Example
```python
few_shot_prompt = """
Human: Classify the sentiment of these tweets as Positive, Negative, or Neutral:

Tweet: "I love the new features in this update! Great job team!"
Sentiment: Positive

Tweet: "The service was down for 3 hours, very frustrating"
Sentiment: Negative

Tweet: "The company released their quarterly earnings report"
Sentiment: Neutral

Tweet: "This product has completely changed how I work, amazing!"
Sentiment: 

Assistant:
"""
```

### Code Generation Example
```python
code_generation_prompt = """
Human: Write Python functions based on these examples:

Example 1:
Input: "Create a function to calculate factorial"
Output: 
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

Example 2:
Input: "Write a function to check if a string is palindrome"
Output:
def is_palindrome(s):
    return s == s[::-1]

Now create: "Write a function to find the maximum number in a list"

Assistant:
"""
```

## 5. Amazon Bedrock Implementation

### Basic Client Setup
```python
import boto3
import json

def get_bedrock_client():
    """Initialize Bedrock client"""
    return boto3.client('bedrock-runtime', region_name='us-east-1')

def invoke_model(prompt, model_id='anthropic.claude-v2', temperature=0.5, max_tokens=200):
    """Invoke Bedrock model with given parameters"""
    client = get_bedrock_client()
    
    body = {
        "prompt": prompt,
        "temperature": temperature,
        "max_tokens_to_sample": max_tokens,
        "stop_sequences": ["\n\nHuman:"]
    }
    
    response = client.invoke_model(
        modelId=model_id,
        body=json.dumps(body)
    )
    
    response_body = json.loads(response['body'].read())
    return response_body['completion']
```

### Complete Demo Function
```python
def run_prompt_demo():
    """Run a comprehensive prompt tuning demo"""
    
    # Test different temperatures
    prompts = [
        {
            "name": "Factual Query - Low Temp",
            "prompt": "Human: Explain the laws of thermodynamics.\n\nAssistant:",
            "temperature": 0.1,
            "max_tokens": 250
        },
        {
            "name": "Creative Writing - High Temp", 
            "prompt": "Human: Write a poem about artificial intelligence in the style of Shakespeare.\n\nAssistant:",
            "temperature": 0.9,
            "max_tokens": 150
        },
        {
            "name": "Technical Explanation - Medium Temp",
            "prompt": "Human: Explain how neural networks work to a 10-year-old.\n\nAssistant:",
            "temperature": 0.5,
            "max_tokens": 200
        }
    ]
    
    for config in prompts:
        print(f"\n{'='*50}")
        print(f"TEST: {config['name']}")
        print(f"Temperature: {config['temperature']}")
        print(f"{'='*50}")
        
        try:
            response = invoke_model(
                prompt=config['prompt'],
                temperature=config['temperature'],
                max_tokens=config['max_tokens']
            )
            print(f"PROMPT: {config['prompt']}")
            print(f"RESPONSE: {response}")
            print(f"{'-'*50}")
        except Exception as e:
            print(f"Error: {e}")

# Run the demo
if __name__ == "__main__":
    run_prompt_demo()
```

## 6. Advanced Prompt Techniques

### Chain-of-Thought Prompting
```python
chain_of_thought = """
Human: A farmer has 15 chickens and 7 rabbits. How many legs are there in total?

Let's think step by step:
1. Chickens have 2 legs each, so 15 chickens have 15 * 2 = 30 legs
2. Rabbits have 4 legs each, so 7 rabbits have 7 * 4 = 28 legs  
3. Total legs = chicken legs + rabbit legs = 30 + 28 = 58 legs

So the total number of legs is 58.

Now solve this: A restaurant has 12 tables with 4 chairs each and 8 tables with 6 chairs each. How many chairs are there total?

Assistant: Let's think step by step:
"""
```

### Role-Playing Prompts
```python
role_play_prompt = """
Human: You are a friendly customer support agent for a tech company. A customer is frustrated because their internet is slow. Write a helpful response that:
- Acknowledges their frustration
- Provides troubleshooting steps
- Offers escalation if needed

Customer message: "My internet has been extremely slow for 3 days and I can't get any work done! This is unacceptable."

Assistant:
"""
```

## 7. Evaluation and Testing

### Prompt Testing Framework
```python
def test_prompt_variations(base_prompt, variations):
    """Test different variations of a prompt"""
    results = []
    
    for i, variation in enumerate(variations):
        print(f"\nTesting variation {i+1}: {variation['description']}")
        
        full_prompt = f"{base_prompt}\n{variation['addition']}\n\nAssistant:"
        
        response = invoke_model(
            prompt=full_prompt,
            temperature=variation.get('temperature', 0.5),
            max_tokens=variation.get('max_tokens', 200)
        )
        
        results.append({
            'variation': variation['description'],
            'prompt': full_prompt,
            'response': response
        })
        
        print(f"Response: {response}")
    
    return results

# Example usage
base_prompt = "Human: Explain the concept of blockchain"
variations = [
    {
        'description': 'Simple explanation',
        'addition': 'Explain it in simple terms that anyone can understand.',
        'temperature': 0.3
    },
    {
        'description': 'Technical explanation', 
        'addition': 'Provide a detailed technical explanation suitable for developers.',
        'temperature': 0.2
    },
    {
        'description': 'Business perspective',
        'addition': 'Focus on the business applications and benefits.',
        'temperature': 0.4
    }
]

# test_prompt_variations(base_prompt, variations)
```

## Best Practices for Prompt Tuning:

1. **Start Simple**: Begin with basic prompts and gradually add complexity
2. **Be Specific**: Clearly define the desired output format and style
3. **Use Examples**: Include few-shot examples when possible
4. **Control Length**: Use `max_tokens` to manage response size
5. **Temperature Settings**:
   - 0.1-0.3: Factual, deterministic responses
   - 0.4-0.7: Balanced creativity and accuracy  
   - 0.8-1.0: Highly creative, varied responses
6. **Iterate**: Test multiple prompt variations to find what works best

This framework should give you a solid foundation for fine-tuning text prompts with Amazon Bedrock!