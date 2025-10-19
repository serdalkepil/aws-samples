import boto3
from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage

def langchain_bedrock_chat():
    """Simple LangChain integration with Amazon Bedrock"""
    
    # Initialize Bedrock chat model
    chat = ChatBedrock(
        model_id="anthropic.claude-3-sonnet-20240229-v1:0",
        model_kwargs={"temperature": 0.1}
    )
    
    # Send message
    messages = [HumanMessage(content="What is AWS Lambda?")]
    response = chat.invoke(messages)
    
    return response.content

def langchain_bedrock_chain():
    """LangChain chain with prompt template"""
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    
    # Create chat model
    model = ChatBedrock(
        model_id="anthropic.claude-3-sonnet-20240229-v1:0",
        model_kwargs={"temperature": 0.1}
    )
    
    # Create prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful AWS expert assistant."),
        ("human", "{question}")
    ])
    
    # Create chain
    chain = prompt | model | StrOutputParser()
    
    # Invoke chain
    response = chain.invoke({"question": "Explain Amazon S3 in simple terms"})
    
    return response

if __name__ == "__main__":
    print("LangChain + Bedrock Chat:")
    print(langchain_bedrock_chat())
    
    print("\nLangChain + Bedrock Chain:")
    print(langchain_bedrock_chain())