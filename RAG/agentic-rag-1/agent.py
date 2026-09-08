import asyncio

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent

load_dotenv()


async def main():

    # 1. Create Claude LLM
    llm = ChatAnthropic(
        model="claude-sonnet-4-5"
    )

    # 2. Connect to MCP Server
    client = MultiServerMCPClient(
        {
            "weather": {
                "command": "python",
                "args": ["mcp_server.py"],
                "transport": "stdio",
            }
        }
    )

    # 3. Get MCP tools
    tools = await client.get_tools()

    # 4. Create agent
    agent = create_agent(
        model=llm,
        tools=tools
    )

    # 5. Ask question
    response = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "What is the weather in Bangalore?"
                }
            ]
        }
    )

    # 6. Print answer
    print(response["messages"][-1].content)


asyncio.run(main())