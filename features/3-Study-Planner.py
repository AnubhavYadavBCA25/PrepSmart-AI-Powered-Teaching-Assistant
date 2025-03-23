import os
import time
import streamlit as st
import google.generativeai as genai
from features.auth import get_user_details
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

user_data = get_user_details()
name = user_data.get("name")
preferred_lang = user_data.get("preferred_lang")

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
generation_config_sp = {
  "temperature": 0.7,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 2000,
  "response_mime_type": "text/plain",
  "frequency_penalty": 0.4,
  "presence_penalty":0.5
}

# System Instruction
system_instructions = f"""
            You are a PrepSmart Study Plan maker, you can design the study plan for students based on their prefference and their need. Try to use
            emojies which give student an effective and attractive study plan. You should provide the reponse related to education only, if student
             ask any other questions like related to finance, healthcare, or any other domain (excluding education), then you should not provide the 
             answer and ask student to ask the question related to education only.

            Student Name is: {name}
            Preferred Language is: {preferred_lang}, study plan will be generated based on the language you choose.

            Important: You should provide the reponse related to education only, if student ask any other question, then you should not provide the answer
            and ask student to ask the question related to education only.
"""

model = genai.GenerativeModel(model_name="gemini-1.5-flash",
                               safety_settings=safety_settings,
                               generation_config=generation_config_sp,
                               system_instruction=system_instructions)

st.header('EduPlanner🗓️', divider='rainbow')
with st.expander("What is EduPlanner?"):
    st.write(f"""EduPlanner is a AI Powered tool that helps you to plan your study schedule. You can customize your schedule based on your upcoming exams and study goals.
            EduPlanner helps you to stay organized and focused on your studies.""")

plan_type = st.selectbox("Select the type of schedule you want to create", ["Study Plan", "Syllabus Roadmap", "Time Management"])
if plan_type == "Study Plan":
    type_of_schedule = st.selectbox("Select the plan time period", ["Daily", "Weekly"])
    if type_of_schedule == "Daily":
        with st.form("study_planner_daily_form"):
            start_time = st.time_input("Start Time*")
            purpose = st.selectbox("Purpose*", ["Study", "Revision", "Exam Practice"])
            subject = st.text_input("Subject*", placeholder="Machine Learning", value=None)
            topic = st.text_input("Topic*", placeholder="Supervised Learning", value=None)
            duration = st.number_input("Duration in hours*")
            additional_info = st.text_area("Additional Information", placeholder="Any additional information you want to add")
            st.markdown("*Required**")
            submit_button = st.form_submit_button("Create Plan")
        
        if submit_button:
            if not start_time or not purpose or not subject or not topic or not duration:
                st.error("Please fill all the required fields")
                st.stop()
            else:
                st.success("Your Entries have been submitted successfully.")
        st.divider()

        with st.spinner("Processing..."):
            if start_time and purpose and subject and topic and duration is not None:
                prompt = f"""
                    Create a study plan for {subject} on {topic} for {duration} hours with the purpose of {purpose} starting at {start_time}.
                    Some additional information: {additional_info}.
                """
                response = model.generate_content(prompt)
                st.subheader(f"Hello {name}, Here is Your Daily {purpose} Plan")
                output_text = response.text
                def stream_output_text():
                    for word in output_text.split(" "):
                        yield word + " "
                        time.sleep(0.02)
                st.write_stream(stream_output_text())
            else:
                st.warning("Please fill all the required fields.")
    else:
        with st.form("study_planner_weekly_form"):
            start_date = st.date_input("Start Date*")
            end_date = st.date_input("End Date*")
            purpose = st.selectbox("Purpose*", ["Study", "Revision", "Exam Practice"])
            subject = st.text_input("Subject*", placeholder="Machine Learning", value=None)
            topic = st.text_input("Topics*", placeholder="Data Visualization, Database or etc.", value=None)
            duration_per_day = st.number_input("Duration in hours per day*")
            additional_info = st.text_area("Additional Information", placeholder="Any additional information you want to add")
            st.markdown("*Required**")
            submit_button = st.form_submit_button("Create Plan")
        
        if submit_button:
            if not start_date or not end_date or not purpose or not subject or not topic or not duration_per_day:
                st.error("Please fill all the required fields")
                st.stop()
            else:
                st.success("Your Entries have been submitted successfully.")
        st.divider()

        with st.spinner("Processing..."):
            if start_date and end_date and purpose and subject and topic and duration_per_day is not None:
                prompt = f"""
                    Create a weekly study plan for {subject} on {topic} for {duration_per_day} hours per day with the purpose of {purpose} starting from {start_date} to {end_date}. Some
                    additional information: {additional_info}.
                """
                response = model.generate_content(prompt)
                st.subheader(f"Hello {name}, Here is Weekly {purpose} Plan")
                output_text = response.text
                def stream_output_text():
                    for word in output_text.split(" "):
                        yield word + " "
                        time.sleep(0.02)
                st.write_stream(stream_output_text())
            else:
                st.warning("Please fill all the required fields.")

elif plan_type == "Syllabus Roadmap":
    with st.form("syllabus_roadmap_form"):
        subject = st.text_input("Subject*", placeholder="Machine Learning", value=None)
        syllabus = st.text_area("Syllabus*", placeholder="Syllabus details", value=None)
        additional_info = st.text_area("Additional Information", placeholder="Any additional information you want to add")
        submit_button = st.form_submit_button("Create Roadmap")
        st.markdown("*Required**")
    
    if submit_button:
        if not subject or not syllabus:
            st.error("Please fill all the required fields")
            st.stop()
        else:
            st.success("Your Entries have been submitted successfully.")
    st.divider()

    with st.spinner("Processing..."):
        if subject and syllabus is not None:
            prompt = f"""
                Create a syllabus roadmap for {subject} with the following details: {syllabus} and additional information: {additional_info}.
            """
            response = model.generate_content(prompt)
            st.subheader(f"Hello {name}, Here is Your Syllabus Roadmap")
            output_text = response.text
            def stream_output_text():
                for word in output_text.split(" "):
                    yield word + " "
                    time.sleep(0.02)
            st.write_stream(stream_output_text())
        else:
            st.warning("Please fill all the required fields.")

else:
    with st.form("time_management_form"):
        start_time = st.time_input("Start Time*")
        end_time = st.time_input("End Time*")
        purpose = st.selectbox("Purpose*", ["Study", "Revision", "Exam Practice"])
        additional_info = st.text_area("Additional Information", placeholder="Any additional information you want to add")
        submit_button = st.form_submit_button("Create Plan")
        st.markdown("*Required**")

    if submit_button:
        if not start_time or not end_time or not purpose:
            st.error("Please fill all the required fields")
            st.stop()
        else:
            st.success("Your Entries have been submitted successfully.")
    st.divider()

    with st.spinner("Processing..."):
        if start_time and end_time is not None and purpose is not None:
            prompt = f"""
                    Create a time management plan for {purpose} starting at {start_time} and ending at {end_time}. Some additional information: {additional_info}.
            """
            response = model.generate_content(prompt)
            st.subheader(f"Hello {name}, Here is Your Time Management Plan")
            output_text = response.text
            def stream_output_text():
                for word in output_text.split(" "):
                    yield word + " "
                    time.sleep(0.02)
            st.write_stream(stream_output_text())
        else:
            st.warning("Please fill all the required fields.")
