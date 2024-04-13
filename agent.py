import getpass
import os

api_key = os.environ.get('CHATGPT_API_KEY')

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo-0125")

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from tools import AddClass, EndConversation, ShowClasses

tools = [AddClass(), EndConversation(), ShowClasses()]

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an assistant in developing bots. Your goal is to talk with the user to understand their needs and then use the tools to define the bot using CMB class. The CMB class is just text explaining one of the bots dialog options (example - 'get yes/no answer', 'ask user about something', 'end conversation').",
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

# Construct the Tools agent
agent = create_tool_calling_agent(llm, tools, prompt)

# Create an agent executor by passing in the agent and tools
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
current_message = ''

while True:
    current_message = input("Enter your message: ")
    agent_executor.invoke({"input": current_message})
