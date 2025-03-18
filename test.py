import streamlit as st
from google.cloud import firestore
from google.cloud.firestore import Client

@st.cache_resource
def get_db():
    db = firestore.Client.from_service_account_json(".streamlit/firestore-key.json")
    return db

def post_general_feedback(db: Client, name, email, rating, feedback):
    payload = {"name":name, "email":email, "rating":rating, "feedback":feedback}
    doc_ref = db.collection("user-general-feedback").document()
    doc_ref.set(payload)
    return 

def post_technical_feedback(db: Client, name, email, subject, description):
    payload = {"name":name, "email":email, "subject":subject, "description":description}
    doc_ref = db.collection("user-technical-feedback").document()
    doc_ref.set(payload)
    return

def post_feature_request(db: Client, name, email, feature_name, description):
    payload = {"name":name, "email":email, "feature_name":feature_name, "description":description}
    doc_ref = db.collection("user-feature-request").document()
    doc_ref.set(payload)
    return

def main():

    st.header("Testing Firestore Database", divider='rainbow')

    db = get_db()

    with st.expander("User General Feedback"):
        feedback_collection = db.collection("user-general-feedback")

        for doc in feedback_collection.stream():
            st.json(doc.to_dict())
    
    with st.expander("User Technical Feedback"):
        feedback_collection = db.collection("user-technical-feedback")

        for doc in feedback_collection.stream():
            st.json(doc.to_dict())

    with st.expander("User Feature Request"):
        feedback_collection = db.collection("user-feature-req-feedback")

        for doc in feedback_collection.stream():
            st.json(doc.to_dict())

    with st.form("db_form"):
        name = st.text_input("Enter Your Name:")
        email = st.text_input("Enter Email:")
        rating = st.radio("Enter Rating:",["Excellent 🤩", "Great 😄", "Good 🙂", "Average ☹️", "Poor 😞"])
        feedback = st.text_area("Feedback Message:")
        submit = st.form_submit_button()

        if submit:
            if not name or not email or not rating or not feedback:
                st.error("Please provide all fields")
                st.stop()
            else:
                post_general_feedback(db,name,email,rating,feedback)
                st.success("Your feedback submitted successfully!")

if __name__ == '__main__':
    main()