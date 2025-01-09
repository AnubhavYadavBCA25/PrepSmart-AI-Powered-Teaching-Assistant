from features.auth import get_user_details

# Get the user details
user_data = get_user_details()

name = user_data.get('name', 'User')
preferred_lang = user_data.get('preferred_lang', 'English')

# Safett Settings
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

############################## System and Model Settings for Personal Mentor Feature ##############################
# Generation Configurations
generation_config_pm = {
  "temperature": 0.4,
  "top_p": 0.95,
  "top_k": 30,
  "max_output_tokens": 500,
  "response_mime_type": "text/plain",
  "frequency_penalty": 0.4,
  "presence_penalty":0.5
}

# System Instructions
system_instructions_pm = {
    f"""You are a Personal Mentor. You can help students with their academic queries and provide them with the best possible solutions.
    You can also provide them with study tips, project ideas and help them with their issues related to studies.
    
    Student Name is: {name}
    Preferred Language is: {preferred_lang}

    Important Note: Make sure to be polite and helpful to the students. Do not provide any harmful or inappropriate content to the students.
    
    How to start:
    1. Greet the student.
    2. You can start by asking the student about their query and provide them with the best possible solution.
    3. Understand the student's query and provide them with the best and positive possible solution.
    4. Remember the previous conversation with the student and provide them with the best possible solution.
    5. Provide response based on query asked by the student.
    """
}

############################## System and Model Settings for Answer Generation Feature ##############################
# Generation Configurations

# System Instructions

############################## System and Model Settings for Question Bank Feature ##############################
# Generation Configurations
generation_config_qb = {
  "temperature": 0.2,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 1000,
  "response_mime_type": "text/plain",
  "frequency_penalty": 0.4,
  "presence_penalty":0.5
}

# System Instructions
system_instructions_qb = {
    '''You are a Question Bank Maker. You can understand the need and conditions of the students and provide them Questions based on their requirements.
        You can provide them with questions on various topics, subjects and help them with their studies.
    '''
}