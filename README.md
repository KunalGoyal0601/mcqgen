# MCQ Generator

An experimental Python project exploring multiple-choice question generation with Hugging Face hosted language models and LangChain.

> **Status:** Prototype / work in progress. The notebook and Python modules have not been validated from a clean environment. Some parts of the original implementation may need debugging before they work end to end.

## Repository layout

```text
mcqgen/
├── notebooks/
│   └── mcq.ipynb
├── src/
│   └── mcqgen/
│       ├── __init__.py
│       ├── logger.py
│       ├── mcqgenerater.py
│       └── utils.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup

1. Create and activate a virtual environment.
2. Install the dependencies:

   ```bash
   python -m venv .venv
   # Windows PowerShell:
   .venv\Scripts\Activate.ps1
   # macOS/Linux:
   # source .venv/bin/activate

   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and add your Hugging Face token. Never commit `.env`.
4. Open `notebooks/mcq.ipynb` in Jupyter or VS Code and run the cells in order.

## Configuration

The original script reads the environment variable `huggingfacehub_api_token`. Set it in your local `.env` file:

```dotenv
huggingfacehub_api_token=your_hugging_face_token_here
```

Do not paste a real token into a notebook cell or commit one to GitHub. If a token was ever committed, revoke it at the provider and create a new one.

## Current limitations

- The repository contains experimental code and an exploratory notebook, not a polished application or tested CLI.
- The script currently demonstrates a basic model prompt rather than a complete configurable MCQ-generation pipeline.
- The helper functions and model/provider configuration need testing against the installed dependency versions.
- No accuracy or quality evaluation is claimed.

## Next steps

- Add a clean, reproducible generation function with input validation.
- Fix and test PDF/text extraction helpers.
- Add a small test suite and a sample input that contains no personal information.
- Pin dependency versions after a successful clean installation.

## Author

Kunal Goyal — [GitHub profile](https://github.com/KunalGoyal0601)
