# resume-cv-generator

## Overview

This project is an automated resume and cover letter generation system built with Python and LangGraph workflows. It processes job descriptions, personal CV data, and generates tailored resumes, cover letters, and formatted PDFs programmatically.

***

## Getting Started

### Prerequisites

You must create and activate a Python virtual environment named **`llm_env`** before running this project, as it relies on packages installed in that environment.

```bash
conda create -n llm_env python=3.10 -y
conda activate llm_env
```


### Required Python Packages

Ensure the environment has these packages installed, which satisfy the imports used in the project:

- `langchain_groq`
- `langchain_core`
- `pandas`
- `numpy`
- `pydantic`
- `python-dotenv`
- `selenium`
- `webdriver-manager`
- `beautifulsoup4`
- `re` (standard library)
- `fpdf`
- `langgraph`
- `pyyaml` or `ruamel.yaml` (for YAML parsing)

You can install dependencies via pip:



***

## Usage

1. **Update your CV data**

Edit `master_cv.yaml` in the project root to update your personal and professional information. This file serves as the source resume data template used by the workflow.
2. **Run the workflow**

The main workflow is defined in `main.py`. It imports all nodes and state definitions, and composes the pipeline.

You can run it with:

```bash
python main.py
```

The workflow reads job URLs (from a file like `job_urls.txt`), processes each URL through a series of nodes (scraping job description text, summarizing, generating cover letters, updating resumes, exporting PDFs), and saves outputs.

***

## Project Structure

- `main.py` : Assembles and runs the workflow.
- `nodes/` : Functions representing each step (scraping, summarizing, generating, exporting).
- `state/` : Contains your `State` class defining the shared state schema.
- `master_cv.yaml` : Your master resume data to customize.
- `job_urls.txt` : Optional input file with URLs of job postings to process.
- `.gitignore` : Ensure `.env` is ignored for sensitive environment variables.

***

## Environment Configuration

Be sure to keep environment variables (API keys, secrets) in a `.env` file and **do not commit this to GitHub**.

Use `.gitignore` to exclude `.env` files:

```
.env
```

The project loads environment variables automatically using `python-dotenv`.

***

## Notes

- Selenium WebDriver is set up to run headless Chrome using `webdriver_manager` for driver management.
- Use the provided YAML templates to structure your CV and project information.
- The rendering step uses `rendercv` inside the conda environment `llm_env`; ensure this environment is active for those commands.

***



