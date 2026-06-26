import anthropic
import json
from docx import Document
import os


def get_resume():
    resume_env = os.getenv("RESUME_TEXT")
    if resume_env:
        return resume_env
    doc = Document("docs/MasterResume.docx")
    full_text = "\n".join([p.text for p in doc.paragraphs])
    return full_text


def main():
    job_boards = [
        "LinkedIn",
        "Indeed",
        "We Work Remotely",
        "Remote.co",
        "FlexJobs",
        "Remotive",
        "Himalayas",
        "Wellfound",
        "Dice",
        "Built In",
        "Jobspresso",
        "Working Nomads",
        "PowerToFly",
        "Greenhouse Job Board",
        "Otta",
    ]

    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    daily_resume_prompt = (
        "Find me the top 10 jobs closest matching my resume using the following job boards "
        + ", ".join(job_boards)
    )

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=8192,
        tool_choice={"type": "tool", "name": "get_jobs"},
        messages=[
            {
                "role": "user",
                "content": f"Full resume text:{get_resume()}\r\n\r\nPrompt: {daily_resume_prompt}",
            }
        ],
        tools=[
            {
                "name": "get_jobs",
                "description": "Get the the closest job matches",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "jobs": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "source": {"type": "string"},
                                    "company": {"type": "string"},
                                    "location": {"type": "string"},
                                    "title": {"type": "string"},
                                    "percent_match": {"type": "number"},
                                    "requirements": {"type": "string"},
                                    "apply_link": {"type": "string"},
                                },
                                "required": [
                                    "source",
                                    "company",
                                    "location",
                                    "title",
                                    "percent_match",
                                    "requirements",
                                    "apply_link",
                                ],
                            },
                        }
                    },
                    "required": ["jobs"],
                    "additionalProperties": False,
                },
            }
        ],
    )

    # 2. Extract and parse the response text safely
    data = response.content[0].input
    jobs_list = data["jobs"]

    for job in jobs_list:
        print("-" * 40)
        print("Source: " + job["source"])
        print("Company: " + job["company"])
        print("Location: " + job["location"])
        print("Title: " + job["title"])
        print("Percent Match: " + str(job["percent_match"]) + "%")
        print("Requirements: " + job["requirements"])
        print("Apply Link: " + job["apply_link"])


if __name__ == "__main__":
    main()
