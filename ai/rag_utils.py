# ai/rag_utils.py
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
import os

def build_vectorstore(docs_dir="docs", out_dir="vectorstore"):
    loader = DirectoryLoader(docs_dir)
    docs = loader.load()
    split = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=50)
    texts = split.split_documents(docs)
    emb = OpenAIEmbeddings()
    db = FAISS.from_documents(texts, emb)
    db.save_local(out_dir)
    print("Saved vectorstore to", out_dir)
