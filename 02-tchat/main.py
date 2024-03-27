# not importing from LLMs like previous because LangChain assumes LLM is completion model
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import HumanMessagePromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationSummaryMemory, FileChatMessageHistory
from dotenv import load_dotenv

load_dotenv()

chat = ChatOpenAI(verbose=True)

# memory_key defines the additional key value name that will be added as inputs 
# return_messages makes sure is not just plain string and is the full history of Object wrappers for messages
memory = ConversationSummaryMemory(
    # chat_memory=FileChatMessageHistory("messages.json"),
    memory_key="messages", 
    return_messages=True,
    llm=chat
)

prompt = ChatPromptTemplate(
    # should expect to recive messages key and content 
    input_variables=["content", "messages"],
    messages=[
        # look at input vairables and find one called messages 
        MessagesPlaceholder(variable_name="messages"),
        HumanMessagePromptTemplate.from_template("{content}")
    ]
)

chain = LLMChain(
    llm=chat,
    prompt=prompt,
    memory=memory,
    verbose=True
)

while True:
    content = input(">> ")

    result = chain({"content": content})
    
    print(result["text"])