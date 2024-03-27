from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
from dotenv import load_dotenv

load_dotenv()

embeddings = OpenAIEmbeddings()
# emb = embeddings.embed_query("Hi there")

# grabs up to 200 characters and then looks for neareast separator and that becomes a chunk so 200 characters at most
text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=200,
    chunk_overlap=0
)

loader = TextLoader("facts.txt")
docs = loader.load_and_split(
    text_splitter=text_splitter
)

db = Chroma.from_documents(
    docs, # telling chroma you want to calculate embeddings for each chunk of text in docs 
    embedding=embeddings, 
    persist_directory="emb" # SQLite database stored in emb dir 
)

results = db.similarity_search(
    "What is an interseting fact about the English language?"
)

for result in results:
    print("\n")
    print(result.page_content)