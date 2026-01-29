# app/rag.py
# Imports
from langchain_community.llms import HuggingFaceHub
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
#from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma


import os
from dotenv import load_dotenv 
load_dotenv() # loads .env when running locally 
os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HUGGINGFACEHUB_API_TOKEN")

CHROMA_DIR = "/chroma"

# Create embedding model
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Sherlock prompt
PROMPT = """
        You are Sherlock Holmes. 
        
        You must answer ONLY using the information provided in the "Context" section. 
        If the answer is not explicitly stated in the context, you MUST reply with: "I don't have enough evidence to answer that." 
        
        You are not allowed to guess, infer, assume, or invent clues. 
        You must treat missing information as missing evidence.

        Context:
        {context}

        Question:
        {question}
    """


# ---------------------------------------------------------
# Load and split a uploaded document to be saved in vector DB
# ---------------------------------------------------------
def create_vector_index(file_path: str):

    # Based on file extension
    if file_path.lower().endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    else:
        loader = TextLoader(file_path)

    # Load the document into memory
    docs = loader.load()

    # Create a text splitter to break the document into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    # Split the loaded document into smaller chunks
    chunks = splitter.split_documents(docs)

    # Save chunks into persistent ChromaDB
    vectordb = Chroma(
        collection_name="case_files",
        embedding_function=embeddings,
        persist_directory="/chroma"   # Docker volume
    )

    vectordb.add_documents(chunks)
    vectordb.persist()

    return "File uploaded successfully!"

# ---------------------------------------------------------
# Find Context
# ---------------------------------------------------------
def find_context(question: str):
    # If the DB does not exist
    if not os.path.exists(CHROMA_DIR):
        return None

    # 2. Load the existing Chroma vector database
    vectordb = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings
    )

    # Retrieve top‑k chunks 
    retriever = vectordb.as_retriever(search_kwargs={"k": 5}) 
    docs = retriever.invoke(question)

    # Combine retrieved chunks into context 
    context = "\n\n".join([d.page_content for d in docs])
    
    return context
    

# ---------------------------------------------------------
# Generate using ChromaDB + LLM
# ---------------------------------------------------------
def generate_answer(question: str) -> str:
   
    context = find_context(question)
    if context is None:
        return "I don't have enough evidence to answer that."
    
    # Build prompt 
    prompt = PromptTemplate(template=PROMPT, input_variables=["context", "question"] ) 
    final_prompt = prompt.format( context=context, question=question )

    # Initialize the LLM (HuggingFaceHub model)
    # Generate the final answer using the retrieved context
    llm = HuggingFaceHub(
        repo_id="mistralai/Mistral-7B-Instruct-v0.2",
        model_kwargs={"temperature": 0}
    )

    # Parse the output cleanly 
    parser = StrOutputParser() 
    
    # Run the LLM 
    raw_output = llm.invoke(final_prompt)
    answer = parser.parse(raw_output)
    # Return the generated answer
    return answer
