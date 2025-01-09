import os
import streamlit as st
import google.generativeai as genai
from features.functions import *
from features.sys_settings import *
from dotenv import load_dotenv
from features.auth import get_user_details

# Get user details
user_data = get_user_details()
name = user_data.get("name")

load_dotenv()

# Load environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KAY")
genai.configure(api_key=GEMINI_API_KEY)

# Load model
model = genai.GenerativeModel(model_name="gemini-1.5-flash-8b",
                              safety_settings=safety_settings,
                              generation_config=generation_config_pm,
                              system_instruction=system_instructions_pm)

st.header('Question Bank📚', divider='rainbow')
with st.expander("What is Question Bank Maker?"):
    st.write("""Question Bank Maker is a AI Powered Feature that allows you to generate questions on any topic of your choice. It helps you to prepare for exams 
             and interviews by generating questions based on the topic you provide.""")
    
with st.form("question_bank_form"):
    subject = st.text_input("Enter the Subject Name:*")
    topic = st.text_input("Enter the Topic Name:*")
    num_questions = st.number_input("Number of Questions to Generate:*", min_value=1, max_value=10)
    type_of_questions = st.selectbox("Type of Questions to Generate:*", ["MCQs", "Short Answer", "Long Answer"])
    purpose = st.selectbox("Purpose of Questions:*", ["Exam Preparation", "Interview Preparation", "Assignment"])
    additional_info = st.text_area("Additional Information:")
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
        st.write(response.text)
    else:
        st.error("Please fill all the required fields.")