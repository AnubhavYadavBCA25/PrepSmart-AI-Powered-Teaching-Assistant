import streamlit as st 
import json
import time
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

credential_path = "E:\PrepSmart AI Powered Teaching Assist\.streamlit\service_account.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

# Function for lottie file
def load_lottie_file(filepath: str):
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)
    
# Function to translate roles between Gemini and Streamlit terminology
def map_role(role):
    if role == "model":
        return "assistant"
    else:
        return role

def fetch_gemini_response(user_query):
    # Use the session's model to generate a response
    response = st.session_state.chat_session.model.generate_content(user_query)
    print(f"Gemini's Response: {response}")
    return response.parts[0].text

# Function for lottie file
def load_lottie_file(filepath: str):
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)
    
# Extract pages from PDF Files
def get_pdf_text(pdf_docs):
    text=""
    for pdf in pdf_docs:
        pdf_reader= PdfReader(pdf)
        for page in pdf_reader.pages:
            text+= page.extract_text()
    return  text

# Split Text into Chunks
def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

# Create Vector Store
def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

# Create Conversational Chain
def get_conversational_chain():

    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-1.5-pro",
                                    temperature=0.3
                                )

    prompt = PromptTemplate(template = prompt_template, input_variables = ["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain

# Get User Input
def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    
    new_db = FAISS.load_local("faiss_index", embeddings,allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)

    chain = get_conversational_chain()

    
    response = chain(
        {"input_documents":docs, "question": user_question}
        , return_only_outputs=True)

    print(response)
    output_text = response["output_text"]
    def stream_output_text():
        for word in output_text.split(" "):
            yield word + " "
            time.sleep(0.05)
    st.write_stream(stream_output_text())