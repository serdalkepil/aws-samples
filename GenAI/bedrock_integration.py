import boto3
import json

def invoke_bedrock_model(prompt, model_id="qwen.qwen3-coder-30b-a3b-v1:0"):
    """Invoke Amazon Bedrock model with a text prompt"""
    bedrock = boto3.client('bedrock-runtime')
    
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "messages": [{"role": "user", "content": prompt}]
    })
    
    response = bedrock.invoke_model(
        body=body,
        modelId=model_id,
        contentType='application/json'
    )
    
    result = json.loads(response['body'].read())
    return result['content'][0]['text']

if __name__ == "__main__":
    prompt = "What is Amazon Web Services?"
    response = invoke_bedrock_model(prompt)

    print(response)