import streamlit as st
import time

from src.resume_parser import extract_resume_text
from src.resume_analyzer import analyze_resume
from src.job_matcher import calculate_job_match
from src.resume_optimizer import optimize_resume
from src.interview_generator import generate_interview_questions

def show_dashboard():

    # ==================================================
    # Dashboard Header
    # ==================================================

    st.html(
        """
        <div class="hero">

            <div class="hero-badge">
                🎯 Your Interview Preparation Dashboard
            </div>

            <h1>
                Your Career<br>
                Dashboard
            </h1>

            <p>
                Choose what you want to do with your resume
                and target job.
            </p>

        </div>
        """
    )

    # ==================================================
    # Job and Resume Information
    # ==================================================

    col1, col2 = st.columns(2)

    with col1:

        st.html(
            """
            <div class="feature-card">

                <div class="feature-icon">
                    🎯
                </div>

                <h3>
                    Target Job
                </h3>

                <p>
                    Your resume is being evaluated against
                    your selected job description.
                </p>

            </div>
            """
        )

    with col2:

        st.html(
            """
            <div class="feature-card">

                <div class="feature-icon">
                    📄
                </div>

                <h3>
                    Resume
                </h3>

                <p>
                    Your uploaded resume is ready for
                    analysis and improvement.
                </p>

            </div>
            """
        )

    st.write("")
    st.write("")

    # ==================================================
    # Feature Selection
    # ==================================================

    st.markdown("### 🚀 Choose What You Want To Do")

    st.caption(
        "Select an option below to continue."
    )

    st.write("")

    col1, col2, col3 = st.columns(3)

    # ==================================================
    # Resume Score Card
    # ==================================================

    with col1:

        st.html(
            """
            <div class="feature-card">

                <div class="feature-icon">
                    📊
                </div>

                <h3>
                    Check Resume Score
                </h3>

                <p>
                    See how closely your resume matches
                    the target job description.
                </p>

            </div>
            """
        )

        if st.button(
            "📊 Check Resume Score",
            key="score_button",
            use_container_width=True
        ):

            st.session_state.dashboard_feature = "score"

            st.rerun()

    # ==================================================
    # Resume Optimizer Card
    # ==================================================

    with col2:

        st.html(
            """
            <div class="feature-card">

                <div class="feature-icon">
                    ✨
                </div>

                <h3>
                    Optimize Your Resume
                </h3>

                <p>
                    Get specific recommendations to improve
                    your resume for this job.
                </p>

            </div>
            """
        )

        if st.button(
            "✨ Optimize Resume",
            key="optimizer_button",
            use_container_width=True
        ):

            st.session_state.dashboard_feature = "optimizer"

            st.rerun()

    # ==================================================
    # Interview Generator Card
    # ==================================================

    with col3:

        st.html(
            """
            <div class="feature-card">

                <div class="feature-icon">
                    🎤
                </div>

                <h3>
                    Generate Interview Questions
                </h3>

                <p>
                    Practice questions personalized to
                    your resume and target job.
                </p>

            </div>
            """
        )

        if st.button(
            "🎤 Generate Questions",
            key="interview_button",
            use_container_width=True
        ):

            st.session_state.dashboard_feature = "interview"

            st.rerun()

    # ==================================================
    # Selected Feature
    # ==================================================

    if "dashboard_feature" not in st.session_state:
        return

    feature = st.session_state.dashboard_feature

    st.write("")
    st.write("")

    # ==================================================
    # RESUME SCORE
    # ==================================================

    if feature == "score":

        st.html(
            """
            <div class="section-title">
                📊 Resume Score
            </div>

            <div class="section-subtitle">
                Checking how well your resume matches
                the target job.
            </div>
            """
        )

        if "job_match" not in st.session_state:

            loading = st.empty()

            steps = [
                "📄 Reading your resume...",
                "🔍 Extracting your skills...",
                "🎯 Comparing with job requirements...",
                "🤖 Calculating your match score...",
                "✨ Finalizing your results..."
            ]

            for step in steps:

                loading.html(
                    f"""
                    <div class="loading-box">

                        <div class="loading-spinner"></div>

                        <div class="loading-text">
                            {step}
                        </div>

                    </div>
                    """
                )

                time.sleep(0.8)

            try:

                # ------------------------------------------
                # Extract Resume Text
                # ------------------------------------------

                resume_text = extract_resume_text(
                    st.session_state.resume_bytes
                )

                # ------------------------------------------
                # Analyze Resume
                # ------------------------------------------

                resume_analysis = analyze_resume(
                    resume_text
                )

                # ------------------------------------------
                # Match Resume With Job
                # ------------------------------------------

                job_match = calculate_job_match(
                    resume_analysis,
                    st.session_state.job_description
                )

                # ------------------------------------------
                # Save Results
                # ------------------------------------------

                st.session_state.resume_analysis = (
                    resume_analysis
                )

                st.session_state.job_match = (
                    job_match
                )

                loading.empty()

                st.rerun()

            except Exception as e:

                loading.empty()

                st.error(
                    "Something went wrong while analyzing "
                    f"your resume: {e}"
                )

        else:

            result = st.session_state.job_match

            score = result["match_score"]

            # ------------------------------------------
            # Score
            # ------------------------------------------

            st.html(
                f"""
                <div class="score-card">

                    <div class="score-number">
                        {score:.0f}%
                    </div>

                    <div class="score-label">
                        Resume Match Score
                    </div>

                </div>
                """
            )

            st.write("")

            # ------------------------------------------
            # Matching Skills
            # ------------------------------------------

            st.subheader("✅ Matching Skills")

            if result["matching_skills"]:

                for skill in result["matching_skills"]:

                    st.success(skill)

            else:

                st.write(
                    "No strong matching skills found."
                )

            # ------------------------------------------
            # Missing Skills
            # ------------------------------------------

            st.subheader("❌ Missing Skills")

            if result["missing_skills"]:

                for skill in result["missing_skills"]:

                    st.error(skill)

            else:

                st.success(
                    "No major missing skills identified."
                )

            # ------------------------------------------
            # Skills To Learn
            # ------------------------------------------

            st.subheader("📚 Skills You Should Learn")

            if result["skills_to_learn"]:

                for skill in result["skills_to_learn"]:

                    st.info(skill)

            else:

                st.success(
                    "Your current skills cover the main requirements."
                )

            # ------------------------------------------
            # Explanation
            # ------------------------------------------

            st.subheader(
                "🧠 Why You Got This Score"
            )

            st.write(
                result["explanation"]
            )

    # ==================================================
    # RESUME OPTIMIZER
    # ==================================================

    elif feature == "optimizer":

        st.html(
            """
            <div class="section-title">
                ✨ Resume Optimizer
            </div>

            <div class="section-subtitle">
                Discover exactly what you can improve
                for your target job.
            </div>
            """
        )

        if "resume_optimization" not in st.session_state:

            loading = st.empty()

            steps = [
                "🎯 Analyzing job requirements...",
                "🔍 Finding skill gaps...",
                "📝 Reviewing your resume wording...",
                "✨ Improving resume bullet points...",
                "🤖 Checking ATS keywords...",
                "🚀 Finalizing your optimization plan..."
            ]

            for step in steps:

                loading.html(
                    f"""
                    <div class="loading-box">

                        <div class="loading-spinner"></div>

                        <div class="loading-text">
                            {step}
                        </div>

                    </div>
                    """
                )

                time.sleep(0.7)

            try:

                # ------------------------------------------
                # Resume Analysis
                # ------------------------------------------

                if "resume_analysis" not in st.session_state:

                    resume_text = extract_resume_text(
                        st.session_state.resume_bytes
                    )

                    st.session_state.resume_analysis = (
                        analyze_resume(resume_text)
                    )

                # ------------------------------------------
                # Job Match
                # ------------------------------------------

                if "job_match" not in st.session_state:

                    st.session_state.job_match = (
                        calculate_job_match(
                            st.session_state.resume_analysis,
                            st.session_state.job_description
                        )
                    )

                # ------------------------------------------
                # Optimize Resume
                # ------------------------------------------

                optimization = optimize_resume(
                    st.session_state.resume_analysis,
                    st.session_state.job_match,
                    st.session_state.job_description
                )

                st.session_state.resume_optimization = (
                    optimization
                )

                loading.empty()

                st.rerun()

            except Exception as e:

                loading.empty()

                st.error(
                    "Something went wrong while optimizing "
                    f"your resume: {e}"
                )

        else:

            result = st.session_state.resume_optimization

            current_score = result["current_score"]

            potential_score = (
                result["realistic_potential_score"]
            )

            # ------------------------------------------
            # Score Comparison
            # ------------------------------------------

            col1, col2 = st.columns(2)

            with col1:

                st.html(
                    f"""
                    <div class="score-card">

                        <div class="score-number">
                            {current_score:.0f}%
                        </div>

                        <div class="score-label">
                            Current Match
                        </div>

                    </div>
                    """
                )

            with col2:

                st.html(
                    f"""
                    <div class="score-card">

                        <div class="score-number">
                            {potential_score:.0f}%
                        </div>

                        <div class="score-label">
                            Realistic Potential
                        </div>

                    </div>
                    """
                )

            st.write("")

            # ------------------------------------------
            # Summary
            # ------------------------------------------

            st.subheader(
                "🧠 Optimization Summary"
            )

            st.write(
                result["summary"]
            )

            # ------------------------------------------
            # High Priority Changes
            # ------------------------------------------

            st.subheader(
                "🔥 High-Priority Changes"
            )

            for index, change in enumerate(
                result["high_priority_changes"],
                start=1
            ):

                with st.expander(
                    f"{index}. {change['area']}"
                ):

                    st.markdown("**Problem**")

                    st.write(
                        change["problem"]
                    )

                    st.markdown(
                        "**Why it matters**"
                    )

                    st.write(
                        change["why_it_matters"]
                    )

                    st.markdown(
                        "**What you should change**"
                    )

                    st.write(
                        change["recommended_change"]
                    )

                    suggested_text = (
                        change["suggested_text"]
                    )

                    if suggested_text.strip():

                        st.markdown(
                            "**Suggested wording**"
                        )

                        st.code(
                            suggested_text
                        )

            # ------------------------------------------
            # ATS Keywords
            # ------------------------------------------

            st.subheader(
                "🔑 ATS Keywords"
            )

            if result["ats_keywords"]:

                for keyword in result["ats_keywords"]:

                    st.info(keyword)

            else:

                st.write(
                    "No additional ATS keywords identified."
                )

            # ------------------------------------------
            # Skills To Learn
            # ------------------------------------------

            st.subheader(
                "📚 Skills To Learn"
            )

            if result["skills_to_learn"]:

                for item in result["skills_to_learn"]:

                    with st.expander(
                        f"📌 {item['skill']}"
                    ):

                        st.write(
                            item["reason"]
                        )

            else:

                st.success(
                    "No additional major skills were identified."
                )

            # ------------------------------------------
            # General Improvements
            # ------------------------------------------

            st.subheader(
                "💡 General Improvements"
            )

            if result["general_improvements"]:

                for improvement in (
                    result["general_improvements"]
                ):

                    st.write(
                        f"• {improvement}"
                    )

            else:

                st.write(
                    "No additional general improvements."
                )

        # ==================================================
    # INTERVIEW GENERATOR
    # ==================================================

    elif feature == "interview":

        st.html(
            """
            <div class="section-title">
                🎤 Interview Generator
            </div>

            <div class="section-subtitle">
                Practice personalized interview questions
                based on your resume and target job.
            </div>
            """
        )

        # ------------------------------------------
        # Interview settings
        # ------------------------------------------

        col1, col2, col3 = st.columns(3)

        with col1:

            interview_type = st.selectbox(
                "Interview Type",
                [
                    "Technical",
                    "HR",
                    "Behavioral",
                    "Project Based",
                    "Mixed"
                ],
                key="interview_type"
            )

        with col2:

            difficulty = st.selectbox(
                "Difficulty",
                [
                    "Easy",
                    "Medium",
                    "Hard"
                ],
                index=1,
                key="interview_difficulty"
            )

        with col3:

            number_of_questions = st.slider(
                "Number of Questions",
                min_value=3,
                max_value=10,
                value=5,
                key="question_count"
            )

        st.write("")

        # ------------------------------------------
        # Generate button
        # ------------------------------------------

        if st.button(
            "🎯 Generate Interview Questions",
            key="generate_interview_button",
            use_container_width=True
        ):

            # Clear previous questions
            if "interview_questions" in st.session_state:
                del st.session_state.interview_questions

            loading = st.empty()

            steps = [
                "📄 Reading your resume...",
                "🎯 Understanding the job requirements...",
                "🧠 Personalizing the questions...",
                "💡 Preparing sample answers...",
                "✨ Finalizing your interview set..."
            ]

            for step in steps:

                loading.html(
                    f"""
                    <div class="loading-box">

                        <div class="loading-spinner"></div>

                        <div class="loading-text">
                            {step}
                        </div>

                    </div>
                    """
                )

                time.sleep(0.7)

            try:

                # ------------------------------------------
                # Make sure resume analysis exists
                # ------------------------------------------

                if "resume_analysis" not in st.session_state:

                    resume_text = extract_resume_text(
                        st.session_state.resume_bytes
                    )

                    st.session_state.resume_analysis = (
                        analyze_resume(resume_text)
                    )

                # ------------------------------------------
                # Generate questions
                # ------------------------------------------

                questions_result = (
                    generate_interview_questions(
                        st.session_state.resume_analysis,
                        st.session_state.job_description,
                        interview_type,
                        difficulty,
                        number_of_questions
                    )
                )

                st.session_state.interview_questions = (
                    questions_result["questions"]
                )

                loading.empty()

                st.rerun()

            except Exception as e:

                loading.empty()

                st.error(
                    "Something went wrong while generating "
                    f"the interview questions: {e}"
                )

        # ------------------------------------------
        # Display questions
        # ------------------------------------------

        if "interview_questions" in st.session_state:

            questions = st.session_state.interview_questions

            st.write("")

            st.subheader(
                "🎤 Your Personalized Interview Questions"
            )

            st.caption(
                f"{len(questions)} questions • "
                f"{interview_type} • "
                f"{difficulty}"
            )

            st.write("")

            for index, item in enumerate(
                questions,
                start=1
            ):

                st.markdown(
                    f"### Question {index}"
                )

                st.write(
                    item["question"]
                )

                st.caption(
                    f"📌 {item['category']}  •  "
                    f"🔥 {item['difficulty']}"
                )

                with st.expander(
                    "💡 View Answer"
                ):

                    st.markdown(
                        "### 📝 Sample Answer"
                    )

                    st.write(
                        item["answer"]
                    )

                    st.markdown(
                        "### 🎯 Why This Answer Is Good"
                    )

                    st.write(
                        item["why_answer_is_good"]
                    )

                    st.markdown(
                        "### 🔑 Key Points To Mention"
                    )

                    for point in item["key_points"]:

                        st.write(
                            f"• {point}"
                        )