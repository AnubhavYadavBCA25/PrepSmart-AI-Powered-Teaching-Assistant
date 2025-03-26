import streamlit as st
import yaml
import json
from yaml.loader import SafeLoader
from streamlit_authenticator.utilities import Hasher, LoginError
import streamlit_authenticator as stauth
from google.cloud import firestore
from google.cloud.firestore import Client
from google.oauth2 import service_account

# Firestore Database
@st.cache_resource
def get_db():
    key_dict = json.loads(st.secrets["textkey"])
    creds = service_account.Credentials.from_service_account_info(key_dict)
    db = Client(credentials=creds, project="prepsmartai-d1457")
    # db = firestore.Client.from_service_account_json(".streamlit/firestore-key.json")
    return db

# Post Registration Data
def post_registration_data(db: Client, name, username, email, password, lang, course, specialization, year_of_study):
    payload = {
        "name":name,
        "username":username,
        "email":email,
        "password":password,
        "language":lang,
        "course":course,
        "specialization":specialization,
        "year_of_study":year_of_study
    }
    doc_ref = db.collection("user-registration").document()
    doc_ref.set(payload)
    return

# Loading config file
with open('config.yaml', 'r', encoding='utf-8') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Ensure config structure
if config is None:
    config = {}
if 'credentials' not in config:
    config['credentials'] = {}
if 'usernames' not in config['credentials']:
    config['credentials']['usernames'] = {}

# Initialize session state for register page
if 'register' not in st.session_state:
    st.session_state['register'] = False
if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = None
if 'user_data' not in st.session_state:
    st.session_state['user_data'] = {}

db = get_db()

def show_login_form():
    # Creating the authenticator object
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
    )
    
    # Creating a login widget
    try:
        authenticator.login()
    except LoginError as e:
        st.error(e)
    
    if st.session_state["authentication_status"]:
        authenticator.logout('Logout', "sidebar")
        st.sidebar.write(f'Welcome **{st.session_state["name"]}**👋')
        # Extract user data
        username = st.session_state["username"]
        user_data = config['credentials']['usernames'].get(username, {})
        st.session_state["user_data"] = user_data
    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')

    # Only show the "Register" button if the user is NOT logged in
    if st.session_state["authentication_status"] is None or st.session_state["authentication_status"] == False:
        st.write("---")
        if st.button("Register"):
            st.session_state['register'] = True  # Switch to register page

# Define function to show the register form
def show_register_form():
    with st.container(border=True):
        st.write("## Register")
        st.divider()
        new_username = st.text_input("Enter Username")
        new_name = st.text_input("Enter Your Full Name")
        new_password = st.text_input("Enter Password", type="password")
        new_email = st.text_input("Enter your email")
        preferred_lang = st.selectbox("Preferred Language",  ["English","Japanese","Korean","Arabic","Bahasa Indonesia","Bengali","Bulgarian","Chinese (Simplified)","Chinese (Traditional)",
                                                            "Croatian","Czech","Danish","Dutch","Estonian","Farsi","Finnish","French","German","Gujarati","Greek","Hebrew","Hindi","Hungarian","Italian","Kannada","Latvian",
                                                            "Lithuanian","Malayalam","Marathi","Norwegian","Polish","Portuguese","Romanian","Russian","Serbian","Slovak","Slovenian","Spanish","Swahili","Swedish","Tamil",
                                                            "Telugu","Thai","Turkish","Ukrainian","Urdu","Vietnamese"])
        course = st.selectbox("Select Your Course:", ['BCA','MCA','BTech','MTech','Bsc','MSc'])
        specialization = st.selectbox("Select You Specialization (If any):", ['Data Science', 'Blockchain', 'AI/ML', 'Cloud Computing', 'None'])
        year_of_study = st.selectbox("Year of Study:", ['1st Year', '2nd Year', '3rd Year', 'Final Year'])
        
        if st.button("Submit Registration"):

            with st.spinner("Registering..."):
                if new_username and new_password and new_email:
                    # Hash the new password
                    hasher = Hasher()
                    hashed_password = hasher.hash(new_password)
                    if 'credentials' not in config:
                        config['credentials'] = {}
                    if 'usernames' not in config['credentials']:
                        config['credentials']['usernames'] = {}
                        
                    # Update the config dictionary
                    config['credentials']['usernames'][new_username] = {
                        'name': new_name,
                        'password': hashed_password,
                        'email': new_email,
                        'preferred_lang': preferred_lang,
                        'course': course,
                        'specialization': specialization,
                        'year_of_study': year_of_study
                    }

                    # Store Data on Firebase
                    post_registration_data(db=db,
                                           name=new_name,
                                           username=new_username,
                                           password=hashed_password,
                                           email=new_email,
                                           lang=preferred_lang,
                                           course=course,
                                           specialization=specialization,
                                           year_of_study=year_of_study)
                
                    # Save the updated credentials to the config.yaml file
                    with open('config.yaml', 'w') as file:
                        yaml.dump(config, file)
                    
            st.success("User registered successfully! You can now log in.")
            st.balloons()

            # Add a "Back to Login" button to return to the login page
    if st.button("Back to Login"):
        st.session_state['register'] = False  # Return to login page

# Main section: Show either login or register form based on state
def authentication():
    if st.session_state['register']:
        show_register_form()  # Show register form
    else:
        show_login_form()  # Show login form

# Get user details
def get_user_details():
    return st.session_state.get("user_data", {})