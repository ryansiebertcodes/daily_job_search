# daily_job_finder

A Python script that uses the Claude API to match your resume against top remote job boards and surface the top 10 best-fit roles daily. Runs automatically via GitHub Actions.

---

## How It Works

1. Reads your resume from `docs/MasterResume.docx` using `python-docx`
2. Sends the resume text + job search prompt to the Claude API (`claude-sonnet-4-6`)
3. Claude returns structured JSON with 10 job matches including title, source, location, match %, requirements, and apply link
4. Results are printed to the console (and eventually emailed as a daily digest)

---

## Project Structure

```
daily_job_finder/
├── src/
│   └── fetch_resumes.py      # Main script
├── docs/
│   └── MasterResume.docx     # Your resume (gitignored)
├── .env                      # API key (gitignored)
├── .gitignore
├── Makefile
├── requirements.txt
└── README.md
```

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/daily_job_finder.git
cd daily_job_finder
```

### 2. Create and activate virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
make install
```

### 4. Add your API key

Create a `.env` file in the project root:

```
ANTHROPIC_API_KEY=sk-ant-xxxxxxxx
```

Get your API key at [console.anthropic.com](https://console.anthropic.com) under **Settings → API Keys**.

### 5. Add your resume

Place your resume at:

```
docs/MasterResume.docx
```

### 6. Run the script

```bash
make run
```

---

## Dependencies

| Package | Purpose |
|---|---|
| `anthropic` | Claude API client |
| `python-docx` | Read resume from .docx file |
| `python-dotenv` | Load `.env` variables |

Install all via:

```bash
pip install -r requirements.txt
```

---

## Claude API Details

- **Model:** `claude-sonnet-4-6`
- **Max tokens:** `8192`
- **Structured output:** Tool use with forced `get_jobs` schema
- **Estimated cost:** ~$0.02 per run (~250 runs on $5)

### Response Schema

```json
{
  "jobs": [
    {
      "source": "LinkedIn",
      "location": "Seattle, WA (Remote)",
      "title": "Senior Data Engineer",
      "percent_match": 97,
      "requirements": "Python, SQL, Snowflake, Azure Data Factory...",
      "apply_link": "https://www.linkedin.com/jobs/search/..."
    }
  ]
}
```

---

## Job Boards Searched

LinkedIn, Indeed, We Work Remotely, Remote.co, FlexJobs, Remotive, Himalayas, Wellfound, Dice, Built In, Jobspresso, Working Nomads, PowerToFly, Greenhouse Job Board, Otta

---

## GitHub Actions (Scheduler)

The script runs daily via GitHub Actions. The workflow file lives at `.github/workflows/daily_job_finder.yml`.

To set up:
1. Push repo to GitHub
2. Go to **Settings → Secrets and variables → Actions**
3. Add secret: `ANTHROPIC_API_KEY`

---

## Important Notes

- Apply links are **pre-filtered search URLs**, not links to individual postings
- The resume file is gitignored — you must add it manually after cloning
- Always run from the **project root** so relative paths resolve correctly
- Makefile requires **tab indentation** (not spaces)

---

## .gitignore

```
venv/
.env
docs/MasterResume.docx
sample_output.txt
__pycache__/
*.pyc
*.pyo
.DS_Store
.vscode/
```
