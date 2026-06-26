# daily_job_search

A Python script that uses the Claude API to match your resume against top remote job boards and surface the top 10 best-fit roles daily. Runs automatically via GitHub Actions every morning at 8am Seattle time (15:00 UTC).

---

## How It Works

1. Reads your resume from the `RESUME_TEXT` GitHub secret (falls back to `docs/MasterResume.docx` for local dev)
2. Sends the resume text + job search prompt to the Claude API (`claude-sonnet-4-6`)
3. Claude returns structured JSON with 10 job matches including title, company, source, location, match %, requirements, and apply link
4. Results are printed to the console (GitHub Actions logs)

---

## Project Structure

```
daily_job_search/
├── .github/
│   └── workflows/
│       └── daily_job_search.yml  # GitHub Actions workflow
├── src/
│   └── fetch_resumes.py          # Main script
├── docs/
│   └── README.md                 # Place MasterResume.docx here for local dev
├── .env                          # API key (gitignored)
├── .gitignore
├── Makefile
├── requirements.txt
└── README.md
```

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/daily_job_search.git
cd daily_job_search
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

### 5. Add your resume (local dev only)

Place your resume at:

```
docs/MasterResume.docx
```

### 6. Run the script locally

```bash
make run
```

---

## Dependencies

| Package | Purpose |
|---|---|
| `anthropic` | Claude API client |
| `python-docx` | Read resume from .docx file (local dev) |
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
      "company": "Acme Corp",
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

## GitHub Actions

The script runs daily at **8am Seattle time (15:00 UTC)** via GitHub Actions.

### Workflow file: `.github/workflows/daily_job_search.yml`

```yaml
name: daily

on:
  # Uncomment push/pull_request triggers for debugging
  # push:
  #   branches: [ "main" ]
  # pull_request:
  #   branches: [ "main" ]
  schedule:
    - cron: '0 15 * * *'

jobs:
  run-job-search:
    runs-on: ubuntu-latest

    steps:
      - name: Check out repository code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run script
        run: python3 src/fetch_resumes.py
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          RESUME_TEXT: ${{ secrets.RESUME_TEXT }}
```

### GitHub Secrets Required

Go to **Settings → Secrets and variables → Actions** and add:

| Secret | Description |
|---|---|
| `ANTHROPIC_API_KEY` | Your Anthropic API key |
| `RESUME_TEXT` | Your resume as plain text |

### Disabling the Schedule

Go to **Actions** → click workflow name → **"..."** menu → **Disable workflow**

### Enabling Push Trigger for Testing

Uncomment the `push` block in the workflow YAML and push to main to trigger a run immediately.

---

## Resume Handling

The script checks for `RESUME_TEXT` environment variable first, then falls back to `docs/MasterResume.docx`:

```python
def get_resume():
    resume_env = os.getenv("RESUME_TEXT")
    if resume_env:
        return resume_env
    doc = Document("docs/MasterResume.docx")
    full_text = "\n".join([p.text for p in doc.paragraphs])
    return full_text
```

This means:
- **GitHub Actions** — uses `RESUME_TEXT` secret (resume never committed to repo)
- **Local dev** — falls back to `docs/MasterResume.docx`

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
