import boto3
import json

# Initialize Bedrock client
bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

# Simple function to call Bedrock
def ask_bedrock(question):
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 500,
        "messages": [{"role": "user", "content": question}]
    })
    
    response = bedrock.invoke_model(
        body=body,
        modelId="anthropic.claude-3-sonnet-20240229-v1:0"
    )
    
    return json.loads(response['body'].read())['content'][0]['text']

# Example usage
if __name__ == "__main__":
    answer = ask_bedrock("What is AWS?")
    print(answer)