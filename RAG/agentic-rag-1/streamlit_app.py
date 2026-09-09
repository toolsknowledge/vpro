import asyncio
import streamlit as st
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent

load_dotenv()

async def get_weather_response(city: str) -> str:
    llm = ChatAnthropic(model="claude-sonnet-4-5")
    client = MultiServerMCPClient({
        "weather": {"command": "python", "args": ["mcp_server.py"], "transport": "stdio"}
    })
    tools = await client.get_tools()
    agent = create_agent(model=llm, tools=tools)
    result = await agent.ainvoke({
        "messages": [{"role": "user", "content": f"What is the weather in {city}?"}]
    })
    return result["messages"][-1].content

st.title("Weather Agent")
city = st.text_input("Enter city name", "Chennai")

if st.button("Get Weather"):
    with st.spinner(f"Fetching weather for {city}..."):
        answer = asyncio.run(get_weather_response(city))
    st.write(answer)