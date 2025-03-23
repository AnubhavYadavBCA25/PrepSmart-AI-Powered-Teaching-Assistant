import streamlit as st
import json
from features.auth import get_user_details
from google.cloud import firestore
from google.cloud.firestore import Client
from google.oauth2 import service_account

# Get user details
user_data = get_user_details()
name = user_data.get("name")
email = user_data.get("email")

# Firestore Database
@st.cache_resource
def get_db():
    key_dict = json.loads(st.secrets["textkey"])
    creds = service_account.Credentials.from_service_account_info(key_dict)
    db = Client(credentials=creds, project="prepsmartai-d1457")
    # db = firestore.Client.from_service_account_json(".streamlit/firestore-key.json")
    return db

# Post General Feedback
def post_general_feedback(db: Client, name, email, rating, feedback):
    payload = {"name":name, "email":email, "rating":rating, "feedback":feedback}
    doc_ref = db.collection("user-general-feedback").document()
    doc_ref.set(payload)
    return 

# Post Technical Feedback
def post_technical_feedback(db: Client, name, email, subject, description):
    payload = {"name":name, "email":email, "subject":subject, "description":description}
    doc_ref = db.collection("user-technical-feedback").document()
    doc_ref.set(payload)
    return

# Post Feature Request
def post_feature_request(db: Client, name, email, feature_name, description):
    payload = {"name":name, "email":email, "feature_name":feature_name, "description":description}
    doc_ref = db.collection("user-feature-req-feedback").document()
    doc_ref.set(payload)
    return

# Main User Interface
st.header('EduConnect📞', divider='rainbow')

db = get_db()

# Category
category = st.selectbox('Enter Query Type:', ['General Feedback', 'Technical Issue', 'Feature Request'])

if category == 'General Feedback':
    with st.form(key='general_feedback'):
        user_name = st.text_input("Your Name:*", value=name)
        user_email = st.text_input("Your Email:*", value=email)
        rating = st.radio("Please Enter Rating:*",["Excellent 🤩", "Great 😄", "Good 🙂", "Average ☹️", "Poor 😞"]) # Use st.feedback
        feedback = st.text_area("Your Feedback:*", placeholder="Enter Your Feedback Here")
        st.markdown("*Required**")
        submit_button = st.form_submit_button("Submit")
    
    if submit_button:
        if not user_name or not user_email or not rating or not feedback:
            st.error("Please fill all the required fields.")
            st.stop()
        else:
            with st.spinner("Submitting Feedback..."):
                post_general_feedback(db, user_name, user_email, rating, feedback)
            st.success("Thank You For Your Feedback.")
            st.balloons()

elif category == 'Technical Issue':
    with st.form(key='technical_issue'):
        user_name = st.text_input("Your Name:*", value=name)
        user_email = st.text_input("Your Email:*", value=email)
        subject = st.text_input("Enter Subject of Issue:*", placeholder="Ex: Facing Issues in Personal Mentor Feature.")
        description = st.text_area("Describe the Issue:*", placeholder="Enter the details of the issue you are facing")
        st.markdown("*Required**")
        submit_button = st.form_submit_button("Submit")
    
    if submit_button:
        if not user_name or not user_email or not subject or not description:
            st.error("Please fill all the required fields.")
            st.stop()
        else:
            with st.spinner("Submitting Issue..."):
                post_technical_feedback(db, user_name, user_email, subject, description)
            st.success("Thank You For Raising an Issue. We will get back to you within 24 hours.")
            st.balloons()

else:
    with st.form(key='feature_request'):
        user_name = st.text_input("Your Name:*", value=name)
        user_email = st.text_input("Your Email:*", value=email)
        feature_name = st.text_input("Enter Feature Name:*", placeholder="Ex: Notes Download Feature")
        description = st.text_area("Describe the Feature:*", placeholder="Enter the details of the feature you want")
        st.markdown("*Required**")
        submit_button = st.form_submit_button("Submit")
    
    if submit_button:
        if not user_name or not user_email or not feature_name or not description:
            st.error("Please fill all the required fields.")
            st.stop()
        else:
            with st.spinner("Submitting Request..."):
                post_feature_request(db, user_name, user_email, feature_name, description)
            st.success("Thank You For Your Request. We will update you soon.")
            st.balloons()
                                   