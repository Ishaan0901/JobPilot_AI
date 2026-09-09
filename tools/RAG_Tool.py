from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.tools import tool
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()


@tool
def RAG_tool(query):
    """
    Retrieves useful information from the user's uploaded resume
    such as technical skills, experience, education, projects, etc.
    """

    project_root = Path(__file__).resolve().parent.parent
    resume_path = project_root / "uploaded_resume.pdf"

    if not resume_path.is_file():
        return f"Resume file not found: {resume_path}"

    # Document Loader
    loader = PyPDFLoader(str(resume_path))
    doc = loader.load()

    # Chunking
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=900,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(doc)

    # Embedding
    embedder = HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-en-v1.5"
    )

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embedder
    )

    # Retriever
    retriever = vector_store.as_retriever(
        search_kwargs={"k": 3}
    )

    # Retrieve relevant documents
    retrieved_docs = retriever.invoke(query)

    # Return readable text to the LLM
    return "\n\n".join(
        doc.page_content for doc in retrieved_docs
    )