# app/rag.py
# Imports...
import os
import chromadb
from dotenv import load_dotenv
import transformers
import torch

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ---------------------------------------------------------
# Environment
# ---------------------------------------------------------
load_dotenv()
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# ---------------------------------------------------------
# Embeddings (LOCK THIS MODEL)
# ---------------------------------------------------------
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-base-en-v1.5"
)

# ---------------------------------------------------------
# Connect to Chroma DB (Docker service)
# ---------------------------------------------------------
chroma_client = chromadb.HttpClient(host="http://chroma:8000")

# Create vector store
vector_store = Chroma(
    client=chroma_client,
    collection_name="case_files",
    embedding_function=embeddings
)

# ---------------------------------------------------------
# Sherlock Prompt (Anti-Hallucination)
# ---------------------------------------------------------
PROMPT = """
You are Sherlock Holmes.

You MUST answer using ONLY the information in the Context.
If the answer is NOT explicitly stated in the Context,
you MUST reply with exactly:

"I don't have enough evidence to answer that."

You are NOT allowed to:
- Use outside knowledge
- Guess
- Infer
- Paraphrase missing facts

Context:
{context}

Question:
{question}

Answer:
"""



# ---------------------------------------------------------
# Indexing: Add a Case File
# ---------------------------------------------------------
def index_document(file_path: str) -> str:
    """
    Load a PDF or text file, split it into chunks,
    and store it in Chroma DB.
    """

    if file_path.lower().endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    else:
        loader = TextLoader(file_path)

    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(documents)

    if not chunks:
        return "No content found in document."

    # Store documents (embeddings are created automatically)
    vector_store.add_documents(chunks)

    # collection = chroma_client.get_collection("case_files")
    # count = collection.count()

    # return f"Indexed {len(chunks)} chunks. Total vectors in DB: {count}"


    return f"Indexed {len(chunks)} chunks successfully."

# ---------------------------------------------------------
# Retrieval
# ---------------------------------------------------------
def retrieve_context(question: str, k: int = 4) -> str | None:
    """
    Retrieve top-k relevant chunks.
    """

    docs = vector_store.similarity_search(question, k=k)

    if not docs:
        return None

    context = "\n\n".join([d.page_content for d in docs])

    return context

# ---------------------------------------------------------
# Question Answering (RAG)
# ---------------------------------------------------------
def answer_question(question: str) -> str:
    """
    Answer a question using RAG.
    """

    context = retrieve_context(question)

    if context is None:
        return "I don't have enough evidence to answer that."

    final_prompt = PromptTemplate(
        template=PROMPT,
        input_variables=[context, question]
    )

    pipeline = transformers.pipeline(
        "text-generation",
        model="meta-llama/Meta-Llama-3.1-8B-Instruct",
        huggingfacehub_api_token=os.environ["HUGGINGFACEHUB_API_TOKEN"],
        model_kwargs={"torch_dtype": torch.bfloat16},
        device_map="auto",
    )

    messages = [
        {"role": "system", "content": context},
        {"role": "user", "content": question},
    ]

    outputs = pipeline(
        messages,
        max_new_tokens=256,
    )
    

    return outputs[0]["generated_text"][-1]
