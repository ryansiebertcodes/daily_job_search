# daily_job_search

A Python script that uses the Claude API to match your resume against top remote job boards and surface the top 10 best-fit roles daily. Runs automatically via GitHub Actions every morning at 8am Seattle time (15:00 UTC). Results are emailed directly to your inbox.

---

## How It Works

1. Reads your resume from the `RESUME_TEXT` GitHub secret (falls back to `docs/MasterResume.docx` for local dev)
2. Sends the resume text + job search prompt to the Claude API (`claude-sonnet-4-6`)
3. Claude returns structured JSON with 10 job matches — filtered by job boards and excluding large companies
4. Results are printed to the console and emailed as a daily digest

---

## Project Structure

```
daily_job_search/
├── .github/
│   └── workflows/
│       └── daily_job_search.yml  # GitHub Actions workflow
├── src/
│   ├── fetch_resumes.py          # Main script
│   └── config.py                 # Job boards and excluded companies
├── docs/
│   └── README.md                 # Place MasterResume.docx here for local dev
├── .env                          # API key and email credentials (gitignored)
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

### 4. Add your credentials

Create a `.env` file in the project root:

```
ANTHROPIC_API_KEY=sk-ant-xxxxxxxx
GMAIL_USER=youremail@gmail.com
GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx
```

Get your Anthropic API key at [console.anthropic.com](https://console.anthropic.com) under **Settings → API Keys**.

For Gmail, generate an App Password at [myaccount.google.com](https://myaccount.google.com) under **Security → App Passwords**.

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

## Configuration (`src/config.py`)

All customizable settings live in `config.py` — no need to touch the main script.

### Job Boards Searched

LinkedIn, Indeed, We Work Remotely, Remote.co, FlexJobs, Remotive, Himalayas, Wellfound, Dice, Built In, Jobspresso, Working Nomads, PowerToFly, Greenhouse Job Board, Otta

### Excluded Companies

Large companies (10,000+ employees) are filtered out to focus on roles where your application is more likely to get personal attention:

Big Tech: Amazon, Microsoft, Google, Meta, Apple, Netflix, Salesforce, Oracle, IBM, SAP, Dell, HP, Intel, Cisco, Nvidia, Adobe, Workday, ServiceNow, Snowflake

Large Consulting: Accenture, Deloitte, McKinsey, PwC, KPMG, EY, Capgemini, Infosys, Wipro, TCS

Large Healthcare/Finance: UnitedHealth, Optum, JPMorgan, Bank of America, Wells Fargo, Citigroup

To add or remove companies, edit `EXCLUDED_COMPANIES` in `src/config.py`.

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

## Email Digest

Results are emailed daily to your Gmail account. The email includes:
- Job title and company
- Source job board
- Location
- Match percentage
- Key requirements
- Apply link (pre-filtered search URL)

Email subject format: `Daily Job Search from Anthropic API for June 26, 2026`

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
          GMAIL_USER: ${{ secrets.GMAIL_USER }}
          GMAIL_APP_PASSWORD: ${{ secrets.GMAIL_APP_PASSWORD }}
```

### GitHub Secrets Required

Go to **Settings → Secrets and variables → Actions** and add:

| Secret | Description |
|---|---|
| `ANTHROPIC_API_KEY` | Your Anthropic API key |
| `RESUME_TEXT` | Your resume as plain text |
| `GMAIL_USER` | Your Gmail address |
| `GMAIL_APP_PASSWORD` | Your Gmail App Password |

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
