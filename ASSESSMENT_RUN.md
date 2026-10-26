# Run and review the assessment version

This branch contains the revised prompts, contact/numeric/HTML safeguards and DOCX export fix. The assessment deployment is https://resumeai-dheeraj-assessment.streamlit.app/. See ASSESSMENT_PROMPTS.md for exact prompts and test status.

## Local setup

Use Python 3.12 and a virtual environment.

```sh
python -m venv .venv
# Windows PowerShell
.venv/Scripts/Activate.ps1
pip install -r requirements.txt
```

Set at least one provider credential in your local environment or Streamlit secret storage. Supported names: GEMINI_KEY_1 through GEMINI_KEY_6, GEMINI_API_KEY, GOOGLE_API_KEY, GROQ_KEY, OPENROUTER_KEY. Gemini defaults to gemini-3.8-flash; GEMINI_MODEL optionally overrides it. Groq defaults to openai/gpt-oss-120b; GROQ_MODEL optionally overrides it. Never commit credentials. A single Gemini key can serve both stages.

For PDF export install the operating-system libraries listed in packages.txt. Linux example:

```sh
sudo apt-get update
sudo apt-get install -y libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf-2.0-0 libffi-dev shared-mime-info
streamlit run app.py
```

On Windows, WeasyPrint also needs Pango available through a supported native installation. DOCX export remains available if PDF rendering dependencies are absent.

## Verification

```sh
python -m unittest discover -p test_accuracy.py -v
```

Upload a fictional resume, paste the synthetic job description from ASSESSMENT_PROMPTS.md, generate, compare each claim and contact field with the source, and reopen both downloads. Do not assume a successful generation message proves factual accuracy or a single-page export.

The deterministic checks cannot detect every unsupported skill or semantic claim. Review the output before use. Uploaded resume text is transmitted to the configured AI providers.

## Assessment submission

The assignment accepts a repository/files with run instructions when online hosting is unavailable. Supply this branch or its ZIP, ASSESSMENT_PROMPTS.md, and your own video of at least two minutes. Explain tools, actual prompt revisions, approach, challenges and observed outcome. Live Gemini-to-Groq fallback completed both stages. PDF and DOCX downloads were reopened successfully. See ASSESSMENT_PROMPTS.md for the latest prompt-refinement results and remaining test limits.


