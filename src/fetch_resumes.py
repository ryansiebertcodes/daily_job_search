import os
from datetime import datetime
from email.mime.text import MIMEText
from smtplib import SMTP

import anthropic
from docx import Document

from config import JOB_BOARDS, EXCLUDED_COMPANIES


def send_email(jobs_list):
    # SMTP Configuration
    SMTP_SERVER = "smtp.gmail.com"  # Replace with actual SMTP server
    SMTP_PORT = 587  # 465 for SSL, 587 for TLS
    USERNAME = os.getenv("GMAIL_USER")
    PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

    email_body = str()
    for job in jobs_list:
        # Append the separator and job details to the body string
        email_body += "-" * 40 + "\n"
        email_body += "Source: " + job["source"] + "\n"
        email_body += "Company: " + job["company"] + "\n"
        email_body += "Location: " + job["location"] + "\n"
        email_body += "Title: " + job["title"] + "\n"
        email_body += f"Percent Match: {job['percent_match']}%\n"
        email_body += "Requirements: " + job["requirements"] + "\n"
        email_body += "Apply Link: " + job["apply_link"] + "\n"

    # Email Details
    sender_email = USERNAME
    receiver_email = USERNAME

    # Current date
    now = datetime.now()

    # Full date name format
    english_date = now.strftime("%B %d, %Y")
    subject = "Daily Job Search from Anthropic API for " + english_date
    body = "Here are the top 10 jobs found by Anthropic API:\r\n" + email_body

    # Create the email
    message = MIMEText(body, "plain")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email

    # Send the email
    with SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()  # Secure connection
        server.login(USERNAME, PASSWORD)
        server.sendmail(sender_email, receiver_email, message.as_string())

    print("Email sent successfully!")


def get_resume():
    resume_env = os.getenv("RESUME_TEXT")
    if resume_env:
        return resume_env
    doc = Document("docs/MasterResume.docx")
    full_text = "\n".join([p.text for p in doc.paragraphs])
    return full_text


def main():
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    daily_resume_prompt = (
        "Find me the top 10 jobs closest matching my resume using the following job boards "
        + ", ".join(JOB_BOARDS)
        + ". Exclude jobs from the following companies: "
        + ", ".join(EXCLUDED_COMPANIES)
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

    # Extract and parse the response text safely
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

    send_email(jobs_list)


if __name__ == "__main__":
    main()
