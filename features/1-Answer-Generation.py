import os
import time
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from features.functions import *
from features.auth import get_user_details

load_dotenv()

# Initializing Env and Credientials
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

credential_path = "E:\PrepSmart AI Powered Teaching Assist\.streamlit\service_account.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

st.header("EduRAG Assitant📖", divider='rainbow')