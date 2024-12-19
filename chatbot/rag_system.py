import os
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chat_models import ChatOpenAI

# PDF 처리 및 벡터화
def process_uploaded_pdf(file):
    loader = PyPDFLoader(file.temporary_file_path())
    pages = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(pages)
    Chroma.from_documents(chunks, embedding_model="openai", persist_directory="chroma_db")

# RAG 기반 응답 생성
def get_rag_response(query):
    db = Chroma(persist_directory="chroma_db")
    retriever = db.as_retriever()
    docs = retriever.get_relevant_documents(query)
    llm = ChatOpenAI(model="gpt-4")
    return llm.predict(f"문서: {docs}\n질문: {query}\n답변:")
