"""Load html from files, clean up, split, ingest into Weaviate."""
import pickle

from langchain.document_loaders import ReadTheDocsLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.faiss import FAISS
import sys, os
from dotenv import load_dotenv
from utils.extend_document_loaders.extendReadTheDocs import ExtendReadTheDocsLoader
import pdb

load_dotenv()


def ingest_docs(
    htmlFolder: str = "langchain.readthedocs.io/en/latest/",
    vectorStoreFilePath: str = "vectorstore.pkl",
):
    """Get documents from web pages."""
    # loader = ReadTheDocsLoader(htmlFolder)
    loader = ExtendReadTheDocsLoader(htmlFolder)
    mainContentTagKey = "div"
    mainContentTagDict = {"class": "mwsgeneric-base-html parbase section"}
    raw_documents = loader.load(mainContentTagKey, mainContentTagDict)
    print(f"============================\n")
    print(f"Split text into chunks")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    documents = text_splitter.split_documents(raw_documents)
    print(f"============================\n")
    print(f"Embedd text")
    embeddings = OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"])
    vectorstore = FAISS.from_documents(documents, embeddings)

    print(f"============================\n")
    print(f"Dumb to pickle")
    # Save vectorstore
    with open(vectorStoreFilePath, "wb") as f:
        pickle.dump(vectorstore, f)
        print(f"=================================")
        print(f"Dump vector embeddings to {vectorStoreFilePath}")


if __name__ == "__main__":
    htmlFolder = sys.argv[1]
    vectorstoreFilePath = sys.argv[2]
    ingest_docs(htmlFolder, vectorstoreFilePath)
