import boto3
import json

def invoke_bedrock_model(prompt, model_id="anthropic.claude-3-sonnet-20240229-v1:0"):
    """Invoke AWS Bedrock model with a text prompt"""
    
    bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
    
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
    prompt = "istanbuldaki en iyi 5 kebapciyi listele"
    response = invoke_bedrock_model(prompt)


    # print response
    print(response)

