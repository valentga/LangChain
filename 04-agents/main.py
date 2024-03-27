from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder
)
from langchain.schema import SystemMessage
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv

from tools.sql import run_query_tool, list_tables, describe_tables_tool
from tools.report import write_report_tool
from handlers.chat_model_start_handler import ChatModelStartHandler

load_dotenv()

handler = ChatModelStartHandler()
chat = ChatOpenAI(
    callbacks=[handler]
) 

tables = list_tables()
#agent_scratchpad is very similar in purpose to memory to capture the message history 
prompt = ChatPromptTemplate(
    messages=[
        SystemMessage(content=(
            "You are an AI that has access to a SQLite database.\n"
            f"The database has tables of: {tables}\n"
            "Do not make any assumptions about what tables exist "
            "or what columns exist. Instead, use the 'describe_tables' function"
        )),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ]
)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
tools = [
    run_query_tool, 
    describe_tables_tool, 
    write_report_tool
]

# this is basically just a chain but with the extra tools functionality 
agent = OpenAIFunctionsAgent(
    llm=chat,
    prompt=prompt,
    tools=tools
)

# repeatedly calls the agent 
# takes a look at the result from agent call and checks to see if it is a request from ChatGPT to run a tool 
# if it is, it will run the tool and send that response from the tool back to ChatGPT
# if not, it will just return the result it got back from ChatGPT 
agent_executor = AgentExecutor(
    agent=agent,
    # verbose=True,
    tools=tools, 
    memory=memory
)

agent_executor(
    "How many orders are there? Write the result to a html report."
)
agent_executor(
    "Repeat the exact same process for users."
)