import streamlit as st
from google.cloud import firestore

db = firestore.Client.from_service_account_json(".streamlit/firestore-key.json")

doc_ref = db.collection("feedback").document("user-general-feedback")
doc_ref2 = db.collection("feedback").document("user-technical-feedback")
doc_ref3 = db.collection("feedback").document("user-feature-req-feedback")

doc = doc_ref.get()
doc2 = doc_ref2.get()
doc3 = doc_ref2.get()

st.subheader("User General Feedback")
st.write("The id is:", doc.id)
st.write("The contents are:", doc.to_dict())

st.subheader("User Technical Feedback")
st.write("The id is:", doc2.id)
st.write("The contents are:", doc2.to_dict())

st.subheader("User Feature Request Feedback")
st.write("The id is:", doc3.id)
st.write("The contents are:", doc3.to_dict())