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
            # Pending
"""

model = genai.GenerativeModel(model_name="gemini-1.5-flash",
                               safety_settings=safety_settings,
                               generation_config=generation_config_sp,
                               system_instruction=system_instructions)

st.header('Study Planner🗓️', divider='rainbow')
with st.expander("What is Study Planner?"):
    st.write(f"""Study Planner is a AI Powered tool that helps you to plan your study schedule. You can customize your schedule based on your upcoming exams and study goals.
            Study Planner helps you to stay organized and focused on your studies.""")

plan_type = st.selectbox("Select the type of schedule you want to create", ["Study Plan", "Syllabus Roadmap", "Time Management"])
if plan_type == "Study Plan":
    type_of_schedule = st.selectbox("Select the plan time period", ["Daily", "Weekly"])
    if type_of_schedule == "Daily":
        with st.form("study_planner_form"):
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
                """
                response = model.generate_content(prompt)
                st.subheader(f"Hello {name}, Here is Your Answer")
                output_text = response.text
                def stream_output_text():
                    for word in output_text.split(" "):
                        yield word + " "
                        time.sleep(0.02)
                st.write_stream(stream_output_text())
            else:
                st.warning("Please fill all the required fields.")
    else:
        pass
    # Pending...
