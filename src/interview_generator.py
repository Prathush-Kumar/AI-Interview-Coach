import json
import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def generate_interview_questions(
    resume_analysis,
    job_description,
    interview_type,
    difficulty,
    number_of_questions
):

    resume_json = json.dumps(
        resume_analysis,
        indent=2
    )

    response = client.responses.create(
        model="gpt-5.6-luna",

        input=[
            {
                "role": "system",
                "content": """
You are an expert technical interviewer and career coach.

Generate personalized interview questions using BOTH:

1. The candidate's resume
2. The target job description

Follow these rules:

- Questions must be relevant to the target job.
- Questions should reflect the candidate's actual resume.
- Never invent experience for the candidate.
- Match the requested interview type.
- Match the requested difficulty.
- Provide a useful sample answer for every question.
- Explain why the answer is good.
- Provide important points the candidate should mention.
- Make questions realistic for an actual interview.
"""
            },
            {
                "role": "user",
                "content": f"""
CANDIDATE RESUME:

{resume_json}


TARGET JOB DESCRIPTION:

{job_description}


INTERVIEW TYPE:

{interview_type}


DIFFICULTY:

{difficulty}


NUMBER OF QUESTIONS:

{number_of_questions}


Generate the interview questions.
"""
            }
        ],

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

    return json.loads(response.output_text)