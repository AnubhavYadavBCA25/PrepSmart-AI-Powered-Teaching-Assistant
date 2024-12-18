import streamlit as st
import streamlit_lottie as st_lottie
from features.functions import load_lottie_file

st.set_page_config(page_title="PrepSmart",
            page_icon=":shark:",
            layout="wide",
            initial_sidebar_state="expanded")

def intro():
    st.header("PrepSmart: AI Powered Teaching Assistant :shark:", divider='rainbow')

    with st.container():
        left_col, right_col = st.columns(2)
        with left_col:
            st.subheader("Welcome to PrepSmart :shark:", divider='rainbow')
            intro = '''
                    **PrepSmart** is an AI powered teaching assistant that helps students to study effectively and prepare for exams.
                    It provides features like Answer Generation, Question Bank, Study Planner, Answer Checker and Student Dashboard.
                    PrepSmart is integrated with Google AI models to provide accurate and reliable results. With PrepSmart, students can
                    study smartly and achieve better results in exams. PrepSmart is a one-stop solution for all your study needs.
                    It able to generate answers for any given text, create question bank, plan study schedule, check answers, any subject
                    and any topic. PrepSmart is a smart study companion for students.
            '''
            st.markdown(intro)

        with right_col:
            robot_assist = load_lottie_file("animations resources/robot_assist.json")
            st_lottie.st_lottie(robot_assist, loop=True, width=500, height=500)

        st.divider()

    with st.container():
        left_col, right_col = st.columns(2)
        with right_col:
            st.subheader("Features of PrepSmart ℹ️", divider='rainbow')
            features = [
                        "**Answer Generation:** PrepSmart can generate answers for any given text based on mark scheme.",
                        "**Question Bank:** PrepSmart can create question bank for any subject and any topic.",
                        "**Study Planner:** PrepSmart can plan study schedule for students.",
                        "**Answer Checker:** PrepSmart can check answers for students and provide feedback.",
                        "**Student Dashboard:** PrepSmart provides student dashboard to track study progress.",
                        "**Contact Us:** PrepSmart provides contact us feature to get in touch with us."
            ]

            for feature in features:
                st.markdown(f"🔹 {feature}")
            st.write("*Explore the features from the sidebar navigation.*")

        with left_col:
            feature_animation = load_lottie_file("animations resources/features.json")
            st_lottie.st_lottie(feature_animation, loop=True, width=500, height=500)

        st.divider()

    with st.container(border=True):
        st.subheader("FAQs❓", divider='rainbow')
        
        # FAQ 1
        with st.expander("What is PrepSmart?"):
            st.write("PrepSmart is an AI powered teaching assistant that helps students to study effectively and prepare for exams.")
        
        # FAQ 2
        with st.expander("What are the features of PrepSmart?"):
            st.write("PrepSmart provides features like Answer Generation, Question Bank, Study Planner, Answer Checker, Student Dashboard and Contact Us.")

        # FAQ 3
        with st.expander("How PrepSmart can help students?"):
            st.write("PrepSmart can help students to study smartly and achieve better results in exams. PrepSmart is a one-stop solution for all your study needs.")

        # FAQ 4
        with st.expander("How to use PrepSmart?"):
            st.write("You can explore the features from the sidebar navigation and use the features as per your requirements.")
        
        # FAQ 5
        with st.expander("How to contact Team PrepSmart?"):
            st.write("You can contact us from the Contact Us feature in the sidebar navigation.")

pg = st.navigation([
    st.Page(intro, title="Home", icon="🏠"),
    st.Page("features/1-Answer-Generation.py", title="Answer Generation", icon="📖"),
    st.Page("features/2-Ques-Bank.py", title="Question Bank", icon="📚"),
    st.Page("features/3-Study-Planner.py", title="Study Planner", icon="🗓️"),
    st.Page("features/4-Ans-Checker.py", title="Answer Checker", icon="🖋️"),
    st.Page("features/Contact-Us.py", title="Contact Us", icon="📞"),
    st.Page("features/Student-Dashboard.py", title="Student Dashboard", icon="🧑🏻‍🎓"),
])

pg.run()