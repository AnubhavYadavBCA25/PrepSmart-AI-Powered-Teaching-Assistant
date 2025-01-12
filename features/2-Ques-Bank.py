import os
import time
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from features.auth import get_user_details

# Get user details
user_data = get_user_details()
name = user_data.get("name")

load_dotenv()

# Load environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KAY")
genai.configure(api_key=GEMINI_API_KEY)

# Safett Settings
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

# Generation Configurations
generation_config_qb = {
  "temperature": 0.2,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 1500,
  "response_mime_type": "text/plain",
  "frequency_penalty": 0.4,
  "presence_penalty":0.5
}

# System Instructions
system_instructions_qb = {
    '''You are a Question Bank Maker. You can understand the need and conditions of the students and provide them Questions based on their requirements.
        You can provide them with questions on various topics, subjects and help them with their studies. Generate questions in proper format. Like: Use
        proper spacing, markdowns and etc. to make question understandable and readable.
        For MCQ type question, write question and then four options in sequence of 4 lines and then their answers.
            
            MCQ Question Example:
            Ques. 1: What is Machine Learning
            A) A subset of Artificial Intelligence
            B) A subset of Data Science
            C) A subset of Computer Science
            D) A subset of Mathematics
            Answer: A) A subset of Artificial Intelligence
    '''
}

# Load model
model = genai.GenerativeModel(model_name="gemini-1.5-flash-8b",
                              safety_settings=safety_settings,
                              generation_config=generation_config_qb,
                              system_instruction=system_instructions_qb)

st.header('Question Bank📚', divider='rainbow')
with st.expander("What is Question Bank Maker?"):
    st.write("""Question Bank Maker is a AI Powered Feature that allows you to generate questions on any topic of your choice. It helps you to prepare for exams 
             and interviews by generating questions based on the topic you provide.""")
    
with st.form("question_bank_form"):
    subject = st.text_input("Enter the Subject Name:*", placeholder="Ex: Data Science, Machine Learning or etc.")
    topic = st.text_input("Enter the Topic Name:*", placeholder="Ex: Linear Regression, Python Programming or etc.")
    num_questions = st.number_input("Number of Questions to Generate:*", min_value=1, max_value=10)
    type_of_questions = st.selectbox("Type of Questions to Generate:*", ["MCQs", "Short Answer", "Long Answer"])
    purpose = st.selectbox("Purpose of Questions:*", ["Exam Preparation", "Interview Preparation", "Assignment"])
    additional_info = st.text_area("Additional Information:", placeholder="Ex: Provide any additional information if required.")
    st.markdown("*Required**")
    submit_button = st.form_submit_button("Generate Questions")

if submit_button:
    if not subject or not topic or not num_questions or not type_of_questions or not purpose:
        st.error("Please fill all the required fields.")
        st.stop()
    else:
        st.success("Your entries have been submitted successfully.")
st.divider()

with st.spinner("Generating Questions..."):
    if subject and topic and num_questions and type_of_questions and purpose is not None:
        prompt = f"""
            Generate {num_questions} {type_of_questions} questions on the topic "{topic}" for the subject "{subject}" for my {purpose}. Additional Information: {additional_info}
            Make sure to provide the best possible questions based on the topic and subject. Generate relevant questions for the topic.
        """
        response = model.generate_content(prompt)
        st.subheader(f"Hello {name}, here are the generated questions for you:")
        output = response.text
        def stream_output():
            for word in output.split(" "):
                yield word + " "
                time.sleep(0.02)
        st.write_stream(stream_output())

    else:
        st.warning("Please fill all the required fields.")