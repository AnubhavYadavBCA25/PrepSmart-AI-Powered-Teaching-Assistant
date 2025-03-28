import streamlit as st
from features.functions import load_lottie_file
import streamlit_lottie as st_lottie

st.header('About Us🧑🏻‍💻', divider='rainbow')

with st.container(border=True):
    left_col, right_col = st.columns(2)
    with left_col:
        st.subheader("Anubhav Yadav", divider='rainbow')
        st.markdown('''
                        - **Role:** Developer
                        - **Email:** [![Anubhav Email](https://img.icons8.com/color/30/email.png)](ay6666@srmist.edu.in)
                        - **LinkedIn:** [![Anubhav Yadav LinkedIn](https://img.icons8.com/color/30/linkedin.png)](https://www.linkedin.com/in/anubhav-yadav-data-science/)
                        - **GitHub:** [![Anubhav Yadav GitHub](https://badgen.net/badge/icon/GitHub?icon=github&label)](https://www.github.com/AnubhavYadavBCA25)
                        - **Bio:** I am a Final Year BCA Data Science student at the SRM Institute of Science and Technology Delhi NCR Campus. I am a Data Science enthusiast 
                            and passionate about learning new technologies. I have experience in Python, Machine Learning, Deep Learning, Data Analysis, Data Visualization,
                            Generative AI and Web Application Development.
                    ''')
    with right_col:
        anubhav_profile = load_lottie_file('animations resources/anubhav_profile.json')
        st_lottie.st_lottie(anubhav_profile, key='anubhav', height=380, width=380 ,loop=True, quality='high')

with st.container(border=True):
    left_col, right_col = st.columns(2)
    with right_col:
        st.subheader("Sparsh Jaiswal", divider='rainbow')
        st.markdown('''
                        - **Role:** Developer
                        - **Email:** [![Sparsh Email](https://img.icons8.com/color/30/email.png)]()
                        - **LinkedIn:** [![Sparsh Jaiswal LinkedIn](https://img.icons8.com/color/30/linkedin.png)](https://http://www.linkedin.com/in/sparsh-jaiswal-aa903730b/)
                        - **GitHub:** [![Sparsh Jaiswal GitHub](https://badgen.net/badge/icon/GitHub?icon=github&label)](https://github.com/sparshjais)
                        - **Bio:** I am a Final Year BCA Data Science student at the SRM Institute of Science and Technology Delhi NCR Campus. With a strong foundation in python
                             and front-end development, Sparsh is dedicated to blending the power of AI with intuitive web design to craft seamless and engaging user experiences.
                    ''')
    with left_col:
        sparsh_profile = load_lottie_file('animations resources/sparsh_profile.json')
        st_lottie.st_lottie(sparsh_profile, key='sparsh', height=380, width=380 ,loop=True, quality='high')
# Footer
st.markdown(
    """
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
    <div style="text-align:center;">
        <p>Made with ❤️ by Team PrepSmart.AI @2025</p>
    </div>
    """, unsafe_allow_html=True
)
