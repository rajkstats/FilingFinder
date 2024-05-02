---
title: FilingFinder
emoji: 👀
colorFrom: green
colorTo: gray
sdk: docker
pinned: false
license: openrail
---

This is the mid-term project for AI Engineering Bootcamp

# FilingFinder 

Welcome to FilingFinder, an innovative application that extracts and interprets key financial data from Meta's 10-K filings using advanced natural language processing techniques. This project is built on Chainlit and designed for financial analysts seeking rapid access to specific financial disclosures.

## Key Components Explained

### `app.py`

- **Environment Setup:** Initializes the environment by loading necessary configurations and environment variables using `dotenv`.
- **Document Loader:** Uses `PyMuPDFLoader` to load the PDF document from a specified URL, which is then processed for data extraction.
- **Text Splitter:** Implements `RecursiveCharacterTextSplitter` to handle text splitting based on token length, ensuring efficient processing of large documents without losing contextual relevance.
- **Vector Store:** Establishes a `Qdrant` vector store to maintain embeddings of the document text, facilitating quick retrieval of information based on query similarity.
- **LLM Integration:** Utilizes `ChatOpenAI` as the language model for generating responses based on the retrieved information, providing a conversational interface.
- **Asynchronous Handling:** Employs asynchronous functions to enhance performance, especially in handling I/O operations like document loading and data querying.

### `requirements.txt`

Lists all the Python dependencies required to run the application, ensuring consistent setup across different environments.

## Usage

To use FilingFinder, launch the application and input your queries related to Meta's financials directly into the interface. The application processes these inquiries to fetch and display relevant information from the 10-K filings.

## Online Demo

Explore FilingFinder in action through our interactive chatbot hosted on Hugging Face:
[Hugging Face App - FilingFinder](https://huggingface.co/spaces/yourusername/filingfinder)

## Contributing

We welcome contributions to improve FilingFinder. Please follow the standard fork-branch-PR workflow to propose changes.