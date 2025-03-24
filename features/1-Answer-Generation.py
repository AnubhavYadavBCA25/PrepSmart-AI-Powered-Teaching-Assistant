import os
import json
import time
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from features.functions import *
from features.auth import get_user_details
from google.oauth2 import service_account

load_dotenv()

# Getting User Detials
user_details = get_user_details()
name = user_details.get("name")
preferred_lang = user_details.get("preferred_lang")


# Initializing Env and Credientials
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# credential_path = "E:\PrepSmart AI Powered Teaching Assist\.streamlit\service_account.json"
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
crediential_path = json.loads(st.secrets["textkey2"])
creds = service_account.Credentials.from_service_account_info(crediential_path)
st.secrets["textkey2"]

# Safety Settings
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

# Generation Configration
generation_config_ag = {
  "temperature": 0.2,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 2000,
  "response_mime_type": "text/plain",
  "frequency_penalty": 0.4,
  "presence_penalty":0.5
}

# System Instruction
system_instructions = {f"""
        You are a EduRAG Answer Generation Assistant, you can help students to generate answers based on Subject, Question, For how much marks you
        need to generate answer. You should provide the reponse related to education only, if student ask any other questions like related to finance,
        healthcare, or any other domain (excluding education), then you should not provide the answer and ask student to ask the question related to education only.
                       
        Student Name is: {name}
        Preferred Language is: {preferred_lang}, answer will be generated based on the language you choose.
        
        If student choose text-based answer, generate the text-based answers based on each and every input given by students and as student choose
        code-based answer, generate the code in copy and paste format and give logic explanation also.
        
        If student choose 'AI-Generated answer', then generated the answer by your own and if student choose 'Notes Extracted Answer', then use RAG
        based concept using LangChain and Gemini model, generate the answer which is given in the uploaded notes.

        Important: You should provide the reponse related to education only, if student ask any other question, then you should not provide the answer
        and ask student to ask the question related to education only.
"""}

# Model
model = genai.GenerativeModel(model_name="gemini-1.5-flash-8b",
                              generation_config=generation_config_ag,
                              safety_settings=safety_settings,
                              system_instruction=system_instructions)

st.header("EduRAG Assitant📖", divider='rainbow')
with st.expander("What is EduRAG?"):
    st.write("""EduRAG is an AI-powered teaching assistant that helps students and teachers with integration of RAG Concept which help students
             to learn and understand the subject matter more effectively. Students can upload their notes and extract the particular content 
             based on question asked by student.""")

ans_type = st.selectbox("Select the Answer Type", ["Text Based Answer", "Code Based Answer"])

# Text-Based Answer Generation
if ans_type == "Text Based Answer":
    generation_type = st.selectbox("Select Answer Generation Type:",['AI Generated Answer','Notes Extracted Answer'])
    if generation_type == 'AI Generated Answer':
        with st.form(key='ai_ans'):
            subject = st.text_input("Enter the Subject*", key="subject_ai", placeholder="Ex: Machine Learning")
            question = st.text_area("Enter the Question*", key="question_ai", placeholder="Ex: What is Machine Learning?", value=None)
            marks = st.number_input("Enter the Marks*", key="marks_ai")
            st.markdown("*Required**")
            submit_button = st.form_submit_button("Check Answer")
        if submit_button:
            if not subject or not question or not marks:
                st.error("Please fill all the fields")
                st.stop()
            else:
                st.success("Your Entries have been submitted successfully.")
        st.divider()
        with st.spinner('Processing...'):
            if subject and question and marks is not None:
                prompt = f"""
                    Generate the Answer for {subject} subject, for {marks} marks and the question is: {question}.
                """
                response = model.generate_content(prompt)
                st.subheader(f"Hello {name}, Here is Your Answer")
                output_ai_text = response.text
                def stream_output_ai_text():
                    for word in output_ai_text.split(" "):
                        yield word + " "
                        time.sleep(0.05)
                st.write_stream(stream_output_ai_text())
            else:
                st.warning("Please fill all the required fields.")

    else:
        with st.form(key='rag_ans'):
            subject = st.text_input("Enter the Subject*", key="subject_rag", placeholder="Ex: Machine Learning")
            question = st.text_area("Enter the Question*", key="question_rag", placeholder="Ex: What is Machine Learning?")
            uploaded_file = st.file_uploader("Choose PDF notes file*", type=["pdf"], accept_multiple_files=True)
            st.markdown("*Required**")
            submit_button = st.form_submit_button("Check Answer")
        if submit_button:
            if not subject or not question or not uploaded_file:
                st.error("Please fill all the fields")
                st.stop()
            else:
                st.success("Your Entries have been submitted successfully.")
        st.divider()
        with st.spinner('Processing...'):
            if subject and question and uploaded_file is not None:
                prompt = f"""
                        {question}
                """
                ## RAG Implementation
                st.subheader(f"Hello {name}, Here is Your Answer")
                raw_text = get_pdf_text(uploaded_file)
                text_chunks = get_text_chunks(raw_text)
                get_vector_store(text_chunks)
                user_input(prompt)
            else:
                st.warning("Please fill all the required fields.")

# Code-Based Answer Generation
else:
    with st.form(key='code_ans'):
        language = st.selectbox("Select Programming Language:*",['Python','Java','JavaScript','C++','C','Go','C#'])
        question = st.text_area("Enter the Question*", key="question_code", placeholder=f"Ex: Write a Python program to add two numbers", value=None)
        additional_info = st.text_area("Enter Additional Info:",key="add_info")
        st.markdown("*Required**")
        submit_button = st.form_submit_button("Check Answer")
    if submit_button:
        if not language or not question:
            st.error("Please fill all the fields")
            st.stop()
        else:
            st.success("Your Entries have been submitted successfully.")
    st.divider()
    with st.spinner('Processing...'):
        if language and question is not None:
            prompt = f"""
                Create a {language} program to {question} and explain the logic of the program separately.
            """
            response = model.generate_content(prompt)
            st.subheader(f"Hello {name}, Here is Your Code")
            output_code = response.text
            def stream_output_code():
                for word in output_code.split(' '):
                    yield word + ' '
                    time.sleep(0.05)
            st.write_stream(stream_output_code())
        else:
            st.warning("Please fill all the required fields.")
