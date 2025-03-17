import streamlit as st
from google.cloud import firestore
from google.cloud.firestore import Client

@st.cache_resource
def get_db():
    db = firestore.Client.from_service_account_json(".streamlit/firestore-key.json")
    return db

def post_message(db: Client, name, email, rating, feedback):
    payload = {"name":name, "email":email, "rating":rating, "feedback":feedback}
    doc_ref = db.collection("feedback").document("user-general-feedback")
    doc_ref.set(payload)
    return 

def main():

    st.header("Testing Firestore Database", divider='rainbow')

    db = get_db()

    with st.expander("Get all feedbacks"):
        feedback_collection = db.collection("feedback")

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
                post_message(db,name,email,rating,feedback)
                st.success("Your feedback submitted successfully!")

if __name__ == '__main__':
    main()