# MCQ Generator

A Python prototype that generates multiple-choice questions from study text using a Hugging Face hosted language model.

## Status

The project has a reusable generation function, PDF/text input helper, JSON response validation, and offline unit tests. Live model generation requires a valid Hugging Face token, network access, and a model/provider available to your account.

## Repository layout

    mcqgen/
    ├── notebooks/mcq.ipynb
    ├── src/mcqgen/
    │   ├── __init__.py
    │   ├── logger.py
    │   ├── mcqgenerater.py
    │   └── utils.py
    ├── tests/test_mcqgen.py
    ├── .env.example
    ├── .gitignore
    ├── requirements.txt
    └── README.md

## Setup

Python 3.10 or newer is recommended.

    python -m venv .venv

Windows PowerShell:

    .venv\Scripts\Activate.ps1

macOS/Linux:

    source .venv/bin/activate

Install dependencies:

    python -m pip install -r requirements.txt

Copy .env.example to .env and set HUGGINGFACEHUB_API_TOKEN to your own token. Keep .env private and never commit a real token. The code also accepts HF_TOKEN or the legacy huggingfacehub_api_token environment variable.

## Run

Open notebooks/mcq.ipynb in Jupyter or VS Code. Run the cells in order, supply study text, then explicitly execute the generation cell. You can also call the function from Python:

    from mcqgen.mcqgenerater import generate_mcqs
    questions = generate_mcqs("Photosynthesis converts light energy into chemical energy.", num_questions=3)
    print(questions)

For a source checkout, add src to PYTHONPATH. The notebook handles the source path when run from the repository root or its notebooks/ folder.

## Input helper

read_file(path) or read_file(open_file) supports UTF-8 .txt and selectable-text .pdf files. Scanned PDFs need OCR. Unsupported extensions raise ValueError.

## Tests

Run the offline tests (no token or model call required):

    python -m unittest discover -s tests -v

Live generation is not part of the offline test suite. Model availability and provider routing can change; check the current Hugging Face model/provider status if the API call fails.

## Limitations

- Questions and answers must be reviewed for factual accuracy and ambiguity.
- Output parsing validates basic structure, not pedagogical quality or whether every answer is supported by the source.
- Long source documents may need chunking; this prototype does not yet implement document chunking or a full evaluation pipeline.
- Never upload confidential or personal study material to a hosted model without permission.

## Author

Kunal Goyal — https://github.com/KunalGoyal0601
