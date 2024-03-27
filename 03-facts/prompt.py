from langchain.vectorstores.chroma import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from redundant_filter_retriever import RedundantFilterRetriever
from dotenv import load_dotenv
import langchain

langchain.debug = True

load_dotenv()

chat = ChatOpenAI()
embeddings = OpenAIEmbeddings()
db = Chroma(
    persist_directory="emb",
    embedding_function=embeddings # need this to create embeddings for user questions 
)
retriever = RedundantFilterRetriever(
    embeddings=embeddings, 
    chroma=db
)

chain = RetrievalQA.from_chain_type(
    llm=chat, 
    retriever=retriever,
    chain_type="stuff" #inject or "stuff" into system message prompt template 
)

result = chain.run("What is an intersting fact about the English Language?")

print(result)