import json
import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def analyze_resume(resume_text):

    response = client.responses.create(
        model="gpt-5.6-luna",

        input=[
            {
                "role": "system",
                "content": """
You are an expert resume analyzer.

Analyze the candidate's resume and extract structured,
accurate information.

Never invent information that is not present in the resume.
"""
            },
            {
                "role": "user",
                "content": f"""
Analyze this resume.

RESUME:
{resume_text}
"""
            }
        ],

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

    return json.loads(response.output_text)