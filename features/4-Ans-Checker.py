import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from features.functions import *
from features.auth import get_user_details

load_dotenv()

# Get user details
user_data = get_user_details()
name = user_data.get("name")

# Load environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

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

# Generation Configurations
generation_config_ac = {
  "temperature": 0.7,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 1500,
  "response_mime_type": "text/plain",
  "frequency_penalty": 0.4,
  "presence_penalty":0.5
}

# System Instructions
system_instructions_ac = {"""
        You are an Answer Checker, you can check both text based and code based answers. You can provide feedback to the students based on their
        answers and help them to improve their answers. You can also provide them with the correct answers and help them to understand the concepts.
        You can also provide them with the best possible solutions to their queries. 
                          
        In Code based answers, you can check the code written by the students and provide them with the correct code and help them to understand the logic.
        Debug the code and provide them with the correct code. Write correct code in copy-paste format, so that students can easily copy the code. And 
        explain the logic of the code separately.
"""}

model = genai.GenerativeModel(model_name="gemini-1.5-pro",
                              safety_settings=safety_settings,
                              generation_config=generation_config_ac,
                              system_instruction=system_instructions_ac)

st.header('Answer Checker🖋️', divider='rainbow')
with st.expander("What is Answer Checker?"):
    st.write("""
        Answer Checker is an AI Powered tool that can check both text based and code based answers. It can provide feedback to the students based on their
        answers and help them to improve their answers. It can also provide them with the correct answers and help them to understand the concepts. For Code
        based answers, it can check the code written by the students and if code is incorrect, it debugs the code and provide them with the correct code with
        logic explanation.""")

# Answer Type
answer_type = st.selectbox("Select the Answer Type", ["Text Based Answer", "Code Based Answer"])
if answer_type == "Text Based Answer":
    with st.form(key='text_ans'):
        subject = st.text_input("Enter the Subject*", key="subject", placeholder="Ex: Machine Learning")
        question = st.text_area("Enter the Question*", key="question", placeholder="Ex: What is Machine Learning?")
        marks = st.number_input("Enter the Marks*", key="marks")
        answer = st.text_area("Enter the Answer*", key="answer", placeholder="Ex: Machine Learning is a subset of AI that allows machines to learn from data.")
        st.markdown("*Required**")
        submit_button = st.form_submit_button("Check Answer")
    
    if submit_button:
        if not subject or not question or not marks or not answer:
            st.error("Please fill all the required fields.")
            st.stop()
        else:
            st.success("Your Entries have been submitted successfully.")
    
    with st.spinner("Checking the Answer..."):
        if subject and question and marks and answer is not None:
            prompt = f"""
                Subject: {subject}
                Question: {question}
                Marks: {marks}
                Answer: {answer}

                Check the answer provided by student for that particular subject, question and marks. Try to give suggestions for making the answer
                more effective and conceptual. Give marks to the student for their provided answer after giving feedback and suggestions.
            """
            response = model.generate_content(prompt)
            st.subheader(f"Hello {name}, Here's Suggestions for your Answer")
            st.write(response.text)
        
        else:
            st.warning("Please fill all the required fields.")

else:
    with st.form('code_ans'):
        language = st.selectbox("Enter Programming Language:*",['Python','Java','JavaScript','C++','C','Go','C#'])
        question = st.text_input("Enter Your Question:*",placeholder="Ex: Create a function to add two numbers.")
        code = st.text_area("Enter Your Code:*", placeholder='''def add(x,y):
        return x+y
        ''')
        purpose = st.multiselect("Enter the Purpose of Check:*",['Optimize Code','Debug Code'])
        error_msg = st.text_input("Any Error Message (If Debugging):", placeholder="Paste the Error Message, Ex: TypeError: unsupported operand type(s) for +: 'int' and 'str'")
        additional_info = st.text_area("Additional Information:", placeholder="Ex: Provide any additional information if required.")
        st.markdown("*Required**")
        submit_button = st.form_submit_button("Submit")

    if submit_button:
        if not language or not question or not code or not purpose:
            st.error("Please fill all the required fields.")
            st.stop()
        else:
            st.success("Your Entries have been submitted successfully.")
    
    with st.spinner("Checking the Code..."):
        if language and question and code and purpose is not None:
            prompt = f"""

            """
            response = model.generate_content(prompt)
            st.subheader(f"Hello {name}, Here is Your Correct Code")
            st.write(response.text)
        
        else:
            st.warning("Please fill all the required fields.")
