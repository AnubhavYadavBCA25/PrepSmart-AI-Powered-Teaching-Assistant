import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from features.functions import *
from features.sys_settings import safety_settings, generation_config_pm, system_instructions_pm

load_dotenv()

# Load environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KAY")
genai.configure(api_key=GEMINI_API_KEY)

# Load model
model = genai.GenerativeModel(model_name="gemini-1.5-pro",
                              safety_settings=safety_settings,
                              generation_config=generation_config_pm,
                              system_instruction=system_instructions_pm)

st.header('Personal Mentor🧑🏻‍🏫', divider='rainbow')

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Display the chat history
for msg in st.session_state.chat_session.history:
    with st.chat_message(map_role(msg["role"])):
        st.markdown(msg["content"])

# Input field for user's message
user_input = st.chat_input("Ask Me Anything...")
if user_input:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_input)

    # Send user's message to Gemini and get the response
    gemini_response = fetch_gemini_response(user_input)

    # Display Gemini's response
    with st.chat_message("assistant"):
        st.markdown(gemini_response)

    # Add user and assistant messages to the chat history
    st.session_state.chat_session.history.append({"role": "user", "content": user_input})
    st.session_state.chat_session.history.append({"role": "model", "content": gemini_response})

# Clear current chat session
with st.sidebar:
    if st.button("Clear Chat"):
        st.session_state.chat_session = model.start_chat(history=[])