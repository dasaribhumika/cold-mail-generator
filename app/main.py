import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text


def create_streamlit_app(llm, portfolio, clean_text):
    # Set background color and font color
    st.markdown(
        """
        <style>
        body {
            background-color: black; /* Black background */
            color: white; /* Default text color */
        }
        .sidebar .sidebar-content {
            background-color: black; /* Black sidebar background */
            color: #f0f0f0; /* Light grey text */
        }
        .sidebar .sidebar-title {
            color: #00ff00; /* Green for sidebar title */
        }
        .stTextInput label {
            color: black; /* White input label */
            font-size: 100px; /* Larger font size for input label */
        }
        .stTextInput input {
            color: black; /* Black text for input */
            background-color: #f0f0f0; /* Light background for input */
        }
        .submit-button {
            display: flex; /* Flexbox to center */
            margin-top: 20px; /* Add some top margin */
        }
        .stButton {
            color: blue; /* Black text color */
            border: none; /* No border */
            border-radius: 5px; /* Rounded corners */
            padding: 10px 20px; /* Padding for button size */
            cursor: pointer; /* Pointer cursor on hover */
            font-size: 16px; /* Button text size */
            width: 200px; /* Fixed width for button */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Sidebar content
    with st.sidebar:
        st.image("img/logo.png", use_column_width=True)  # Replace with your image URL
        st.title("Project Overview")
        st.write(
            """
            ### Cold Mail Generator
            This application helps you generate personalized cold emails for job opportunities.
            Simply enter a job URL, and the app will extract relevant information to create a tailored email.
            """
        )

    # Main content
    st.title("📧 Cold Mail Generator")
    
    # URL input field
    url_input = st.text_input("Enter a URL:", value="https://jobs.nike.com/job/R-33460", key="url_input")

    # Submit button centered in a div
    with st.container():
        st.markdown("<div class='submit-button'>", unsafe_allow_html=True)  # Centering container
        if st.button("Submit"):
            try:
                loader = WebBaseLoader([url_input])
                data = clean_text(loader.load().pop().page_content)
                portfolio.load_portfolio()
                jobs = llm.extract_jobs(data)
                for job in jobs:
                    skills = job.get('skills', [])
                    links = portfolio.query_links(skills)
                    email = llm.write_mail(job, links)
                    st.code(email, language='markdown')
            except Exception as e:
                st.error(f"An Error Occurred: {e}")
        st.markdown("</div>", unsafe_allow_html=True)  # End centering container


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)
