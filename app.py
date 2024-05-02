# Importing Python libraries
import os
import asyncio
from dotenv import load_dotenv

import chainlit as cl

from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ChatMessageHistory, ConversationBufferMemory
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.vectorstores import Qdrant
from langchain_openai import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import tiktoken

# Load environment variables from a .env file
load_dotenv()

@cl.on_chat_start
async def start_chat():
    # Notify the user that the system is setting up the vector store
    await cl.Message(content="Setting up Qdrant vector store. Please wait...").send()

    # Load documents using PyMuPDFLoader from the specified URL
    docs = PyMuPDFLoader("https://d18rn0p25nwr6d.cloudfront.net/CIK-0001326801/c7318154-f6ae-4866-89fa-f0c589f2ee3d.pdf").load()

    # Define a function to calculate the token length using tiktoken
    def tiktoken_len(text):
        tokens = tiktoken.encoding_for_model("gpt-3.5-turbo").encode(text)
        return len(tokens)

    # Configure a text splitter that handles large documents
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 200,  # Ensure there is no cutoff at the edges of chunks
        length_function = tiktoken_len,
    )

    # Split the document into manageable chunks
    split_chunks = text_splitter.split_documents(docs)

    # Set up the embedding model for document encoding
    embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")

    # Asynchronously create a Qdrant vector store with the document chunks
    qdrant_vectorstore = await cl.make_async(Qdrant.from_documents)(
        split_chunks, 
        embedding_model, 
        location=":memory:",  # Use in-memory storage for vectors
        collection_name="meta_10k"  # Name of the collection in Qdrant
    )

    # Initialize a retriever from the Qdrant vector store
    qdrant_retriever = qdrant_vectorstore.as_retriever()

    # Notify the user that setup is complete
    await cl.Message(content="Qdrant setup complete. You can now start asking questions!").send()

    # Initialize a message history to track the conversation
    message_history = ChatMessageHistory()

    # Set up memory to hold the conversation context and return answers
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        output_key="answer",
        chat_memory=message_history,
        return_messages=True,
    )

    # Configure the LLM for generating responses
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, streaming=True)

    # Create a retrieval chain combining the LLM and the retriever
    chain = ConversationalRetrievalChain.from_llm(
        llm,
        retriever=qdrant_retriever,
        chain_type="stuff",  # Specify the type of chain (customizable based on application)
        memory=memory,
        return_source_documents=True
    )

    # Store the configured chain in the user session
    cl.user_session.set("chain", chain)

@cl.on_message
async def main(message: cl.Message):
    # Retrieve the conversational chain from the user session
    chain = cl.user_session.get("chain")
    # Define a callback handler for asynchronous operations
    cb = cl.AsyncLangchainCallbackHandler()

    # Process the incoming message using the conversational chain
    res = await chain.acall(message.content, callbacks=[cb])
    answer = res["answer"]  # Extract the answer from the response

    # Send the processed answer back to the user
    await cl.Message(content=answer).send()
