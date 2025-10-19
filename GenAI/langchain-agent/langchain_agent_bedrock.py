from langchain_aws import ChatBedrock
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
import requests

# Define tools
@tool
def calculator(expression: str) -> str:
    """Calculate mathematical expressions. Use math notation like '5*4' or '10/2'"""
    try:
        return str(eval(expression))
    except:
        return "Invalid expression"

@tool
def weather_info(city: str) -> str:
    """Get weather information for a city"""
    return f"Weather in {city}: 22°C, Sunny"

@tool
def aws_service_info(service: str) -> str:
    """Get information about AWS services"""
    services = {
        "lambda": "AWS Lambda is a serverless compute service",
        "s3": "Amazon S3 is object storage service",
        "ec2": "Amazon EC2 provides virtual servers"
    }
    return services.get(service.lower(), f"No info available for {service}")

def create_bedrock_agent():
    """Create LangChain agent with Bedrock"""
    
    # Initialize Bedrock model
    llm = ChatBedrock(
        model_id="anthropic.claude-3-sonnet-20240229-v1:0",
        model_kwargs={"temperature": 0.1}
    )
    
    # Define tools
    tools = [calculator, weather_info, aws_service_info]
    
    # Create prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. Use tools when needed."),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}")
    ])
    
    # Create agent
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools)
    
    return agent_executor

if __name__ == "__main__":
    agent = create_bedrock_agent()
    
    # Test queries
    queries = [
        "What is 15 * 8?",
        "Tell me about AWS Lambda",
        "What's the weather in Istanbul?"
    ]
    
    for query in queries:
        print(f"\nQuery: {query}")
        result = agent.invoke({"input": query})
        print(f"Answer: {result['output']}")