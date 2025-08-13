import os
import asyncio
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()

async def main():
    # Get absolute path for mathserver.py
    mathserver_path = os.path.abspath("mcp files/mathserver.py")
    # Define the MCP client with correct config
    client = MultiServerMCPClient(
        {
            "math": {
                "transport": "stdio",             
                "command": "python",               
                "args": [mathserver_path]           s
            },
            "weather": {
                "transport": "streamable_http",     
                "url": "http://localhost:8000/mcp"  # ensure this server is running
            }
        }
    )

    # Set the API key for OpenAI
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

    # Get the tools from both servers
    tools = await client.get_tools()

    # Create the agent
    model = ChatOpenAI(model='gpt-4')
    agent = create_react_agent(model, tools)

    # Send a test query to the math server
    math_response = await agent.ainvoke(
    {"messages": [{"role": "user", "content": "what's (3+5) x 12"}]}
)
    print("Math response:", math_response['messages'][-1].content)

    weather_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what is the weather of bangalore"}]}
    )

    print("weather response:", weather_response['messages'][-1].content)
    
# Run the main async function
asyncio.run(main())
