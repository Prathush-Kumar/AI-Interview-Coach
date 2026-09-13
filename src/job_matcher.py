import json
import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def calculate_job_match(resume_analysis, job_description):

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
You are an expert ATS resume and job matching system.

Compare the candidate's resume against the job description.

Calculate a realistic match score from 0 to 100.

Do not give a high score simply to make the candidate happy.

Only consider skills and experience that are actually present
in the resume.

Clearly identify missing skills and useful skills to learn.
"""
            },

            {
                "role": "user",
                "content": f"""
RESUME:

{resume_json}


JOB DESCRIPTION:

{job_description}
"""
            }
        ],

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

    return json.loads(response.output_text)