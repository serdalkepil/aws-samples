import boto3
import json

class BedrockIntegration:
    def __init__(self, region='us-east-1'):
        self.client = boto3.client('bedrock-runtime', region_name=region)
    
    def invoke_claude(self, prompt, max_tokens=1000):
        """Invoke Anthropic Claude model"""
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": prompt}]
        })
        
        response = self.client.invoke_model(
            body=body,
            modelId="anthropic.claude-3-sonnet-20240229-v1:0",
            contentType='application/json'
        )
        
        result = json.loads(response['body'].read())
        return result['content'][0]['text']
    
    def invoke_titan(self, prompt, max_tokens=512):
        """Invoke Amazon Titan Text model"""
        body = json.dumps({
            "inputText": prompt,
            "textGenerationConfig": {
                "maxTokenCount": max_tokens,
                "temperature": 0.7
            }
        })
        
        response = self.client.invoke_model(
            body=body,
            modelId="amazon.titan-text-express-v1",
            contentType='application/json'
        )
        
        result = json.loads(response['body'].read())
        return result['results'][0]['outputText']
    
    def invoke_llama(self, prompt, max_tokens=512):
        """Invoke Meta Llama model"""
        body = json.dumps({
            "prompt": prompt,
            "max_gen_len": max_tokens,
            "temperature": 0.5
        })
        
        response = self.client.invoke_model(
            body=body,
            modelId="meta.llama2-13b-chat-v1",
            contentType='application/json'
        )
        
        result = json.loads(response['body'].read())
        return result['generation']

# Usage example
if __name__ == "__main__":
    bedrock = BedrockIntegration()
    
    prompt = "Explain AWS Bedrock in one sentence."
    
    # Test different models
    claude_response = bedrock.invoke_claude(prompt)
    print(f"Claude: {claude_response}")
    
    titan_response = bedrock.invoke_titan(prompt)
    print(f"Titan: {titan_response}")
    
    llama_response = bedrock.invoke_llama(prompt)
    print(f"Llama: {llama_response}")