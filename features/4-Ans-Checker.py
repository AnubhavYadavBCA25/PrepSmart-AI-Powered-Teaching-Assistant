import os
import time
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from features.auth import get_user_details

load_dotenv()

# Get user details
user_data = get_user_details()
name = user_data.get("name")
preferred_lang = user_data.get("preferred_lang")

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
system_instructions_ac = {f"""
        You are an Answer Checker, you can check both text based and code based answers. You can provide feedback to the students based on their
        answers and help them to improve their answers. You can also provide them with the correct answers and help them to understand the concepts.
        You can also provide them with the best possible solutions to their queries. You should provide the reponse related to education only, if 
        student ask any other questions like related to finance, healthcare, or any other domain (excluding education), then you should not provide 
        the answer and ask student to ask the question related to education only.
                          
        Student Name is: {name}
        Preferred language is: {preferred_lang}, answers will be checked based on the language you choose.
                          
        In Code based answers, you can check the code written by the students and provide them with the correct code and help them to understand the logic.
        Debug the code and provide them with the correct code. Write correct code in copy-paste format, so that students can easily copy the code. And 
        explain the logic of the code separately.
                          
        Important: You should provide the reponse related to education only, if student ask any other question, then you should not provide the answer
        and ask student to ask the question related to education only.
"""}

model = genai.GenerativeModel(model_name="gemini-1.5-pro",
                              safety_settings=safety_settings,
                              generation_config=generation_config_ac,
                              system_instruction=system_instructions_ac)

st.header('EduGrade🖋️', divider='rainbow')
with st.expander("What is EduGrade?"):
    st.write("""
        EduGrade is an AI Powered tool that can check both text based and code based answers. It can provide feedback to the students based on their
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
                Check the answer for the subject {subject} for the question {question} for {marks} marks. The answer provided by the student is: {answer}.
                Analyze the answer based on the question and marks, then provide the feedback to the student. Give some score to the answer and provide the
                effective answer to the student.
            """
            response = model.generate_content(prompt)
            st.subheader(f"Hello {name}, Here's Suggestions for your Answer")
            output_text = response.text
            def stream_output_text():
                for word in output_text.split(" "):
                    yield word + " "
                    time.sleep(0.05)
            st.write_stream(stream_output_text())
        
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
                Check the code for the question {question} in {language} language. The code provided by the student is: 
                {code}.
                If the code is incorrect, then debug the code and provide the correct code with logic explanation. And if
                the code is correct, then provide the feedback to the student that how to optimize the code. Perform is based
                on the purpose selected by the user which is {purpose}. 
            """
            response = model.generate_content(prompt)
            st.subheader(f"Hello {name}, Here is Your Correct Code")
            output_code = response.text
            def stream_output_code():
                for word in output_code.split(" "):
                    yield word + " "
                    time.sleep(0.05)
            st.write_stream(stream_output_code())
        
        else:
            st.warning("Please fill all the required fields.")
