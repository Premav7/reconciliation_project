import os
import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools.file_tools import analyze_reconciliation_data # Import the correct tool here
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")



def get_reconciliation_agent():
    """
    Creates and returns a reconciliation agent that uses a tool for analysis.
    """
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=GEMINI_API_KEY,
        temperature=0.3
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are an expert financial reconciliation agent. Your task is to analyze ERP and bank statement data.

                You will receive the raw content of two files as strings. Use the `analyze_reconciliation_data` tool to perform the core reconciliation logic.

                Your final output should be the structured JSON object returned by the tool. Do not try to analyze the data yourself; rely entirely on the tool's output.
                """
            ),
            ("user", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )

    tools = [analyze_reconciliation_data]
    agent = create_tool_calling_agent(llm, tools, prompt)
    
    return AgentExecutor(agent=agent, tools=tools, verbose=True)

