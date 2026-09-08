from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.tools import tool
from dotenv import load_dotenv
load_dotenv()


@tool
def RAG_tool(resume,query):
    '''
    This is the RAG tool which gets the resume of the user and retrieves useful information from it 
    like technical skills , experience , education etc .
    '''

#   Document Loader:
    loader=PyPDFLoader(resume)
    doc=loader.load()


#   chunking:
    splitter=RecursiveCharacterTextSplitter(chunk_size=900,chunk_overlap=50)
    chunks=splitter.split_documents(doc)


#   Embedding:
    embedder = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
    )
    VectorStore = Chroma.from_documents(
    documents=chunks,
    embedding=embedder
)


#   Retriever:
    retriever = VectorStore.as_retriever(
    search_kwargs={"k": 3}
    )


#   Retrieving Docs:
    retrieved_docs=retriever.invoke(query)


#   Return the retrieved info:
    return retrieved_docs
