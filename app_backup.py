import streamlit as st
import pymupdf
import json
from dotenv import load_dotenv
from openai import OpenAI
import os


# Load environment variables
load_dotenv()

# Create OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
if "resume_analysis" not in st.session_state:
    st.session_state.resume_analysis = None
if "job_match" not in st.session_state:
    st.session_state.job_match = None


st.set_page_config(
    page_title="AI Interview Coach",
    page_icon="🎯",
    layout="wide"
)


st.title("🎯 AI Interview Coach")

st.write(
    "Upload your resume and let AI analyze your skills, "
    "education, projects, and experience."
)
st.subheader("🎯 Target Job")

job_description = st.text_area(
    "Paste the Job Description",
    height=250,
    placeholder="Paste the job description here..."
)
st.subheader("🎤 Interview Settings")

interview_type = st.selectbox(
    "Choose Interview Type",
    [
        "Technical",
        "HR",
        "Behavioral",
        "Project Based",
        "Mixed"
    ]
)

difficulty = st.selectbox(
    "Choose Difficulty",
    [
        "Easy",
        "Medium",
        "Hard"
    ]
)

number_of_questions = st.slider(
    "Number of Questions",
    min_value=3,
    max_value=10,
    value=5
)
uploaded_file = st.file_uploader(
    "Upload your resume",
    type=["pdf"]
)


if uploaded_file is not None:

    st.success("Resume uploaded successfully!")

    # ---------------------------------------
    # STEP 1: Extract text from PDF
    # ---------------------------------------

    pdf_document = pymupdf.open(
        stream=uploaded_file.read(),
        filetype="pdf"
    )

    resume_text = ""

    for page in pdf_document:
        resume_text += page.get_text()

    pdf_document.close()

    # ---------------------------------------
    # STEP 2: Display extracted text
    # ---------------------------------------

    with st.expander("📄 View Extracted Resume Text"):
        st.text_area(
            "Resume Content",
            resume_text,
            height=400
        )

    # ---------------------------------------
    # STEP 3: Analyze Resume with AI
    # ---------------------------------------

    if st.button("🤖 Analyze Resume"):

        if not os.getenv("OPENAI_API_KEY"):
            st.error(
                "OPENAI_API_KEY is missing. "
                "Please add it to your .env file."
            )
            st.stop()

        with st.spinner("AI is analyzing your resume..."):

            try:

                response = client.responses.create(
                    model="gpt-5.6-luna",

                    instructions="""
                    You are an expert technical recruiter
                    and resume analyzer.

                    Analyze the provided resume carefully.

                    Extract only information that is actually
                    present in the resume.

                    Do not invent skills, education, projects,
                    experience, or certifications.

                    Return the information using the required
                    structured format.
                    """,

                    input=f"""
                    Analyze this resume:

                    {resume_text}
                    """,

                    text={
                        "format": {
                            "type": "json_schema",
                            "name": "resume_analysis",
                            "strict": True,
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "name": {
                                        "type": "string"
                                    },
                                    "email": {
                                        "type": "string"
                                    },
                                    "phone": {
                                        "type": "string"
                                    },
                                    "summary": {
                                        "type": "string"
                                    },
                                    "skills": {
                                        "type": "array",
                                        "items": {
                                            "type": "string"
                                        }
                                    },
                                    "education": {
                                        "type": "array",
                                        "items": {
                                            "type": "string"
                                        }
                                    },
                                    "projects": {
                                        "type": "array",
                                        "items": {
                                            "type": "string"
                                        }
                                    },
                                    "experience": {
                                        "type": "array",
                                        "items": {
                                            "type": "string"
                                        }
                                    },
                                    "certifications": {
                                        "type": "array",
                                        "items": {
                                            "type": "string"
                                        }
                                    }
                                },
                                "required": [
                                    "name",
                                    "email",
                                    "phone",
                                    "summary",
                                    "skills",
                                    "education",
                                    "projects",
                                    "experience",
                                    "certifications"
                                ],
                                "additionalProperties": False
                            }
                        }
                    }
                )

                # Convert AI response to Python dictionary
                analysis = json.loads(response.output_text)
                st.session_state.resume_analysis = analysis

                # ---------------------------------------
                # STEP 4: Display results
                # ---------------------------------------

                st.subheader("👤 Candidate")

                st.write(
                    f"**Name:** {analysis['name']}"
                )

                st.write(
                    f"**Email:** {analysis['email']}"
                )

                st.write(
                    f"**Phone:** {analysis['phone']}"
                )

                st.subheader("📝 Summary")

                st.write(
                    analysis["summary"]
                )

                st.subheader("🛠️ Skills")

                for skill in analysis["skills"]:
                    st.write(f"• {skill}")

                st.subheader("🎓 Education")

                for education in analysis["education"]:
                    st.write(f"• {education}")

                st.subheader("🚀 Projects")

                for project in analysis["projects"]:
                    st.write(f"• {project}")

                st.subheader("💼 Experience")

                for experience in analysis["experience"]:
                    st.write(f"• {experience}")

                st.subheader("🏆 Certifications")

                for certification in analysis["certifications"]:
                    st.write(f"• {certification}")

            except Exception as e:

                st.error(
                    f"Something went wrong: {str(e)}"
                )
                st.divider()

st.subheader("🎯 Job Match Analysis")

if st.button("📊 Check Job Match"):

    if st.session_state.resume_analysis is None:
        st.warning("Please analyze your resume first.")

    elif not job_description.strip():
        st.warning("Please paste a job description first.")

    else:

        resume_data = st.session_state.resume_analysis

        with st.spinner("Comparing your resume with the job..."):

            try:

                response = client.responses.create(

                    model="gpt-5.6-luna",

                    instructions="""
                    You are an expert technical recruiter.

                    Compare the candidate's resume with the
                    provided job description.

                    Identify:
                    1. Matching skills
                    2. Missing skills
                    3. Job match score from 0 to 100
                    4. Important skills the candidate should learn
                    5. Short explanation of the match

                    Do not claim that the candidate has a skill
                    unless it is present in the resume.
                    """,

                    input=f"""
                    CANDIDATE RESUME:

                    {json.dumps(resume_data, indent=2)}

                    JOB DESCRIPTION:

                    {job_description}
                    """,

                    text={
                        "format": {
                            "type": "json_schema",
                            "name": "job_match_analysis",
                            "strict": True,
                            "schema": {
                                "type": "object",
                                "properties": {

                                    "match_score": {
                                        "type": "number"
                                    },

                                    "matching_skills": {
                                        "type": "array",
                                        "items": {
                                            "type": "string"
                                        }
                                    },

                                    "missing_skills": {
                                        "type": "array",
                                        "items": {
                                            "type": "string"
                                        }
                                    },

                                    "skills_to_learn": {
                                        "type": "array",
                                        "items": {
                                            "type": "string"
                                        }
                                    },

                                    "explanation": {
                                        "type": "string"
                                    }
                                },

                                "required": [
                                    "match_score",
                                    "matching_skills",
                                    "missing_skills",
                                    "skills_to_learn",
                                    "explanation"
                                ],

                                "additionalProperties": False
                            }
                        }
                    }
                )

                match_result = json.loads(
                    response.output_text
                )
                st.session_state.job_match = match_result

                st.success(
                    f"Job Match Score: "
                    f"{match_result['match_score']:.0f}%"
                )

                st.subheader("✅ Matching Skills")

                if match_result["matching_skills"]:

                    for skill in match_result["matching_skills"]:
                        st.write(f"• {skill}")

                else:
                    st.write("No strong matching skills found.")

                st.subheader("❌ Missing Skills")

                if match_result["missing_skills"]:

                    for skill in match_result["missing_skills"]:
                        st.write(f"• {skill}")

                else:
                    st.write("No major missing skills identified.")

                st.subheader("📚 Skills to Learn")

                for skill in match_result["skills_to_learn"]:
                    st.write(f"• {skill}")

                st.subheader("📝 Analysis")

                st.write(
                    match_result["explanation"]
                )

            except Exception as e:

                st.error(
                    f"Job matching failed: {str(e)}"
                )
                st.divider()


                # ---------------------------------------
# AI INTERVIEW QUESTION GENERATOR
# ---------------------------------------

st.divider()

st.subheader("🎤 AI Interview Question Generator")


if st.button("🎯 Generate Interview Questions"):

    if st.session_state.resume_analysis is None:

        st.warning(
            "Please analyze your resume first."
        )

    elif not job_description.strip():

        st.warning(
            "Please paste a job description first."
        )

    else:

        resume_data = st.session_state.resume_analysis

        with st.spinner(
            "AI is preparing your interview questions..."
        ):

            try:

                response = client.responses.create(

                    model="gpt-5.6-luna",

                    instructions="""
                    You are an experienced technical interviewer
                    and interview coach.

                    Generate realistic interview questions for
                    the candidate based on their resume and
                    target job description.

                    For every question, also provide:

                    1. A strong sample answer.
                    2. An explanation of why the answer is good.
                    3. Important points the candidate should mention.

                    Important rules:

                    - Questions must be relevant to the resume.
                    - Questions must be relevant to the job.
                    - Do not invent projects or skills.
                    - Do not claim that the candidate has skills
                      that are not present in the resume.
                    - Sample answers should be realistic for a
                      fresher.
                    - Do not make answers unnecessarily long.
                    - Answers should help the candidate understand
                      how to answer in a real interview.
                    - For project questions, use the candidate's
                      actual projects.
                    - For behavioral questions, use realistic
                      fresher-level examples.
                    """,

                    input=f"""
                    CANDIDATE RESUME:

                    {json.dumps(
                        resume_data,
                        indent=2
                    )}

                    TARGET JOB DESCRIPTION:

                    {job_description}

                    INTERVIEW TYPE:

                    {interview_type}

                    DIFFICULTY:

                    {difficulty}

                    NUMBER OF QUESTIONS:

                    {number_of_questions}
                    """,

                    text={
                        "format": {
                            "type": "json_schema",
                            "name": "interview_questions",
                            "strict": True,

                            "schema": {

                                "type": "object",

                                "properties": {

                                    "questions": {

                                        "type": "array",

                                        "items": {

                                            "type": "object",

                                            "properties": {

                                                "question": {
                                                    "type": "string"
                                                },

                                                "category": {
                                                    "type": "string"
                                                },

                                                "difficulty": {
                                                    "type": "string"
                                                },

                                                "answer": {
                                                    "type": "string"
                                                },

                                                "why_answer_is_good": {
                                                    "type": "string"
                                                },

                                                "key_points": {

                                                    "type": "array",

                                                    "items": {
                                                        "type": "string"
                                                    }
                                                }

                                            },

                                            "required": [
                                                "question",
                                                "category",
                                                "difficulty",
                                                "answer",
                                                "why_answer_is_good",
                                                "key_points"
                                            ],

                                            "additionalProperties": False
                                        }
                                    }

                                },

                                "required": [
                                    "questions"
                                ],

                                "additionalProperties": False
                            }
                        }
                    }
                )

                questions_data = json.loads(
                    response.output_text
                )


                st.success(
                    "Interview questions generated successfully!"
                )


                st.subheader(
                    "🎤 Your Interview Questions"
                )


                for index, item in enumerate(
                    questions_data["questions"],
                    start=1
                ):

                    st.markdown(
                        f"### Question {index}"
                    )

                    st.write(
                        item["question"]
                    )

                    st.caption(
                        f"Category: {item['category']} | "
                        f"Difficulty: {item['difficulty']}"
                    )


                    # View Answer button
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
                            "### 🔑 Key Points to Mention"
                        )

                        for point in item["key_points"]:

                            st.write(
                                f"• {point}"
                            )


            except Exception as e:

                st.error(
                    f"Question generation failed: {str(e)}"
                )
                # ---------------------------------------
# AI RESUME OPTIMIZER
# ---------------------------------------

st.divider()

st.subheader("🚀 AI Resume Optimizer")

st.write(
    "Get specific recommendations to improve your resume "
    "for the selected job."
)


if st.button("✨ Optimize My Resume"):

    if st.session_state.resume_analysis is None:

        st.warning(
            "Please analyze your resume first."
        )

    elif st.session_state.job_match is None:

        st.warning(
            "Please run Job Match Analysis first."
        )

    elif not job_description.strip():

        st.warning(
            "Please paste a job description first."
        )

    else:

        resume_data = st.session_state.resume_analysis

        match_data = st.session_state.job_match

        with st.spinner(
            "AI is finding the best improvements for your resume..."
        ):

            try:

                response = client.responses.create(

                    model="gpt-5.6-luna",

                    instructions="""
                    You are an expert resume consultant,
                    ATS specialist, and technical recruiter.

                    Analyze the candidate's resume against
                    the target job description.

                    The goal is to identify realistic changes
                    that could improve the candidate's job match.

                    VERY IMPORTANT:

                    Never tell the candidate to add a skill,
                    technology, certification, project, or
                    experience that they do not actually have.

                    Separate recommendations into:

                    1. Changes they can make immediately using
                       information already present in their resume.

                    2. Skills they should learn before adding
                       them to their resume.

                    3. Resume wording improvements.

                    4. Missing ATS keywords.

                    For every recommendation explain:

                    - What is missing
                    - Why it matters
                    - What the candidate should change
                    - A suggested version

                    Do not guarantee a 95-100 score.

                    Estimate a realistic potential score after
                    applying the recommended resume changes,
                    assuming the candidate genuinely has the
                    relevant skills and experience.

                    Prioritize the most important improvements.
                    """,

                    input=f"""
                    CANDIDATE RESUME:

                    {json.dumps(
                        resume_data,
                        indent=2
                    )}

                    CURRENT JOB MATCH ANALYSIS:

                    {json.dumps(
                        match_data,
                        indent=2
                    )}

                    TARGET JOB DESCRIPTION:

                    {job_description}
                    """,

                    text={
                        "format": {

                            "type": "json_schema",

                            "name": "resume_optimization",

                            "strict": True,

                            "schema": {

                                "type": "object",

                                "properties": {

                                    "current_score": {
                                        "type": "number"
                                    },

                                    "realistic_potential_score": {
                                        "type": "number"
                                    },

                                    "summary": {
                                        "type": "string"
                                    },

                                    "high_priority_changes": {

                                        "type": "array",

                                        "items": {

                                            "type": "object",

                                            "properties": {

                                                "area": {
                                                    "type": "string"
                                                },

                                                "problem": {
                                                    "type": "string"
                                                },

                                                "why_it_matters": {
                                                    "type": "string"
                                                },

                                                "recommended_change": {
                                                    "type": "string"
                                                },

                                                "suggested_text": {
                                                    "type": "string"
                                                }

                                            },

                                            "required": [
                                                "area",
                                                "problem",
                                                "why_it_matters",
                                                "recommended_change",
                                                "suggested_text"
                                            ],

                                            "additionalProperties": False
                                        }
                                    },

                                    "ats_keywords": {

                                        "type": "array",

                                        "items": {
                                            "type": "string"
                                        }
                                    },

                                    "skills_to_learn": {

                                        "type": "array",

                                        "items": {

                                            "type": "object",

                                            "properties": {

                                                "skill": {
                                                    "type": "string"
                                                },

                                                "reason": {
                                                    "type": "string"
                                                }

                                            },

                                            "required": [
                                                "skill",
                                                "reason"
                                            ],

                                            "additionalProperties": False
                                        }
                                    },

                                    "general_improvements": {

                                        "type": "array",

                                        "items": {
                                            "type": "string"
                                        }
                                    }

                                },

                                "required": [
                                    "current_score",
                                    "realistic_potential_score",
                                    "summary",
                                    "high_priority_changes",
                                    "ats_keywords",
                                    "skills_to_learn",
                                    "general_improvements"
                                ],

                                "additionalProperties": False
                            }
                        }
                    }
                )

                optimization = json.loads(
                    response.output_text
                )

                # ---------------------------------------
                # DISPLAY SCORE
                # ---------------------------------------

                st.subheader(
                    "📊 Resume Improvement Potential"
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.metric(
                        "Current Score",
                        f"{optimization['current_score']:.0f}%"
                    )

                with col2:

                    st.metric(
                        "Potential Score",
                        f"{optimization['realistic_potential_score']:.0f}%"
                    )


                st.info(
                    optimization["summary"]
                )


                # ---------------------------------------
                # HIGH PRIORITY CHANGES
                # ---------------------------------------

                st.subheader(
                    "🔥 High Priority Changes"
                )

                for index, change in enumerate(
                    optimization["high_priority_changes"],
                    start=1
                ):

                    st.markdown(
                        f"### {index}. {change['area']}"
                    )

                    st.write(
                        "**Problem:**"
                    )

                    st.write(
                        change["problem"]
                    )

                    st.write(
                        "**Why it matters:**"
                    )

                    st.write(
                        change["why_it_matters"]
                    )

                    st.write(
                        "**What you should change:**"
                    )

                    st.write(
                        change["recommended_change"]
                    )

                    st.write(
                        "**Suggested text:**"
                    )

                    st.code(
                        change["suggested_text"],
                        language="text"
                    )


                # ---------------------------------------
                # ATS KEYWORDS
                # ---------------------------------------

                st.subheader(
                    "🔎 Important ATS Keywords"
                )

                for keyword in optimization["ats_keywords"]:

                    st.write(
                        f"• {keyword}"
                    )


                # ---------------------------------------
                # SKILLS TO LEARN
                # ---------------------------------------

                st.subheader(
                    "📚 Skills You Should Learn"
                )

                for skill in optimization["skills_to_learn"]:

                    st.markdown(
                        f"**{skill['skill']}**"
                    )

                    st.write(
                        skill["reason"]
                    )


                # ---------------------------------------
                # GENERAL IMPROVEMENTS
                # ---------------------------------------

                st.subheader(
                    "📝 General Resume Improvements"
                )

                for improvement in optimization[
                    "general_improvements"
                ]:

                    st.write(
                        f"• {improvement}"
                    )


            except Exception as e:

                st.error(
                    f"Resume optimization failed: {str(e)}"
                )