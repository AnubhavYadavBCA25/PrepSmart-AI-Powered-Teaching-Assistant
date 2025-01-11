import streamlit as st
from features.auth import get_user_details

# Get user details
user_data = get_user_details()
name = user_data.get("name")
email = user_data.get("email")

st.header('Contact Us📞', divider='rainbow')

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
            st.success("Thank You For Your Feedback.")

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
            st.success("Thank You For Raising an Issue. We will get back to you within 24 hours.")

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
            st.success("Thank You For Your Request. We will update you soon.")
                                   