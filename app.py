import streamlit as st
import time
from textwrap import dedent
from ui.styles import load_css
from ui.dashboard import show_dashboard


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="AI Interview Coach",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

load_css()
# --------------------------------------------------
# Dashboard
# --------------------------------------------------

if st.session_state.get("page") == "dashboard":
    show_dashboard()
    st.stop()


# --------------------------------------------------
# Session state
# --------------------------------------------------

if "page" not in st.session_state:
    st.session_state.page = "landing"


# --------------------------------------------------
# Hero
# --------------------------------------------------

st.html(
    dedent("""
    <div class="hero">
        <div class="hero-badge">
            ✨ AI-Powered Career Preparation
        </div>

        <h1>
            Prepare Smarter.<br>
            Interview Better.
        </h1>

        <p>
            Analyze your resume, match it with your target job,
            improve your resume and practice personalized interview
            questions with AI.
        </p>
    </div>
    """)
)


# --------------------------------------------------
# Job Description
# --------------------------------------------------

st.html(
    dedent("""
    <div class="section-title">
        🎯 Enter Your Target Job
    </div>

    <div class="section-subtitle">
        Tell us about the job you're applying for.
    </div>
    """)
)

job_description = st.text_area(
    "Job Description",
    height=220,
    placeholder=(
        "Paste the complete job description here...\n\n"
        "Example:\n"
        "We are looking for a Python developer with experience "
        "in machine learning, SQL and cloud technologies."
    ),
    label_visibility="collapsed"
)


# --------------------------------------------------
# Resume Upload
# --------------------------------------------------

st.html(
    dedent("""
    <div class="section-title">
        📄 Upload Your Resume
    </div>

    <div class="section-subtitle">
        Upload your latest resume in PDF format.
    </div>
    """)
)

uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf"],
    label_visibility="collapsed"
)


# --------------------------------------------------
# Uploaded Resume
# --------------------------------------------------

if uploaded_file:

    st.html(
        dedent(f"""
        <div class="feature-card">

            <div class="feature-icon">
                📄
            </div>

            <h3>
                {uploaded_file.name}
            </h3>

            <p>
                Your resume is ready to be analyzed.
                Click the button below to continue.
            </p>

        </div>
        """)
    )


# --------------------------------------------------
# Analyze
# --------------------------------------------------

st.write("")

if st.button(
    "🚀 Analyze My Resume",
    use_container_width=True
):

    if not job_description.strip():

        st.warning(
            "Please enter the job description first."
        )

    elif not uploaded_file:

        st.warning(
            "Please upload your resume first."
        )

    else:

        loading_placeholder = st.empty()

        steps = [
            "📄 Reading your resume...",
            "🔍 Extracting skills and experience...",
            "🎯 Understanding the job requirements...",
            "🤖 Preparing AI analysis...",
            "✨ Almost ready..."
        ]

        for step in steps:

            loading_placeholder.html(
                dedent(f"""
                <div class="loading-box">

                    <div class="loading-spinner"></div>

                    <div class="loading-text">
                        {step}
                    </div>

                </div>
                """)
            )

            time.sleep(0.7)

        loading_placeholder.empty()

        st.success(
            "Resume uploaded successfully! 🎉"
        )
        st.session_state.job_description = job_description
        st.session_state.resume_bytes = uploaded_file.getvalue()
        st.session_state.resume_name = uploaded_file.name

        st.session_state.page = "dashboard"

        st.rerun()


# --------------------------------------------------
# Features
# --------------------------------------------------

st.write("")
st.write("")

st.html(
    dedent("""
    <div class="section-title">
        💼 What You Can Do
    </div>

    <div class="section-subtitle">
        Everything you need to prepare for your target role.
    </div>
    """)
)


col1, col2, col3 = st.columns(3)


# --------------------------------------------------
# Resume Score
# --------------------------------------------------

with col1:

    st.html(
        dedent("""
        <div class="feature-card">

            <div class="feature-icon">
                📊
            </div>

            <h3>
                Resume Score
            </h3>

            <p>
                Find out how well your resume matches
                the job description and discover your
                skill gaps.
            </p>

        </div>
        """)
    )


# --------------------------------------------------
# Resume Optimizer
# --------------------------------------------------

with col2:

    st.html(
        dedent("""
        <div class="feature-card">

            <div class="feature-icon">
                ✨
            </div>

            <h3>
                Resume Optimizer
            </h3>

            <p>
                Get specific recommendations to improve
                your resume without adding skills or
                experience you don't have.
            </p>

        </div>
        """)
    )


# --------------------------------------------------
# Interview Practice
# --------------------------------------------------

with col3:

    st.html(
        dedent("""
        <div class="feature-card">

            <div class="feature-icon">
                🎤
            </div>

            <h3>
                Interview Practice
            </h3>

            <p>
                Generate personalized interview questions
                based on your resume and the target job.
            </p>

        </div>
        """)
    )