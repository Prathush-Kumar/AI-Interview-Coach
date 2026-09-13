import json
import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def optimize_resume(resume_analysis, job_match, job_description):

    resume_json = json.dumps(
        resume_analysis,
        indent=2
    )

    match_json = json.dumps(
        job_match,
        indent=2
    )

    response = client.responses.create(
        model="gpt-5.6-luna",

        input=[
            {
                "role": "system",
                "content": """
You are an expert resume optimization and ATS specialist.

Your job is to help a candidate improve their resume
for a specific job description.

IMPORTANT RULES:

1. Never invent skills, experience, projects,
   certifications or technologies.

2. Never tell the candidate to claim something
   they have not actually done.

3. Separate realistic resume improvements from
   skills the candidate needs to learn.

4. Give specific, actionable changes.

5. Improve wording so that existing experience
   is clearer and more relevant to the target job.

6. Identify useful ATS keywords from the job description.

7. Calculate a realistic potential score after
   making the recommended changes.

8. Never guarantee a 95-100 score.

9. If the resume already contains a skill,
   recommend better positioning instead of
   telling the candidate to learn it again.
"""
            },

            {
                "role": "user",
                "content": f"""
Here is the candidate's resume analysis:

{resume_json}


Here is the current job match analysis:

{match_json}


Here is the target job description:

{job_description}


Create a detailed resume optimization plan.
"""
            }
        ],

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

    return json.loads(response.output_text)