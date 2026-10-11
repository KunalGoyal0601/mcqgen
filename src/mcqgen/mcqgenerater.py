"""Generate multiple-choice questions using a Hugging Face hosted model."""
import json
import os
from typing import Any
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

load_dotenv()
DEFAULT_MODEL = "Qwen/Qwen2.5-7B-Instruct"

def parse_mcqs(text: str) -> list[dict[str, Any]]:
    """Parse and minimally validate a JSON list, allowing a Markdown code fence."""
    cleaned = text.strip()
    fence = chr(96) * 3
    if cleaned.startswith(fence):
        first_newline = cleaned.find("\n")
        if first_newline >= 0:
            cleaned = cleaned[first_newline + 1:]
        if cleaned.rstrip().endswith(fence):
            cleaned = cleaned.rstrip()[:-3].rstrip()
    start, end = cleaned.find("["), cleaned.rfind("]")
    if start < 0 or end < start:
        raise ValueError("Model response did not contain a JSON array of MCQs.")
    try:
        data = json.loads(cleaned[start:end + 1])
    except json.JSONDecodeError as exc:
        raise ValueError(f"Model returned invalid MCQ JSON: {exc}") from exc
    if not isinstance(data, list) or not data:
        raise ValueError("Model response must be a non-empty JSON array.")
    required = {"question", "options", "answer", "explanation"}
    for index, item in enumerate(data, start=1):
        if not isinstance(item, dict) or not required.issubset(item):
            raise ValueError(f"MCQ {index} must contain: {', '.join(sorted(required))}.")
        if not isinstance(item["options"], list) or len(item["options"]) < 2:
            raise ValueError(f"MCQ {index} must contain at least two options.")
        if not all(isinstance(item[key], str) and item[key].strip()
                   for key in ("question", "answer", "explanation")):
            raise ValueError(f"MCQ {index} has an empty question, answer, or explanation.")
        if item["answer"] not in item["options"]:
            raise ValueError(f"MCQ {index} answer must match one of its options.")
    return data

def generate_mcqs(context: str, num_questions: int = 5,
                  model_name: str = DEFAULT_MODEL, token: str | None = None) -> list[dict[str, Any]]:
    """Generate structured MCQs from supplied study text using a hosted model."""
    if not isinstance(context, str) or not context.strip():
        raise ValueError("context must be a non-empty string.")
    if not isinstance(num_questions, int) or not 1 <= num_questions <= 30:
        raise ValueError("num_questions must be an integer between 1 and 30.")
    api_token = token or os.getenv("HUGGINGFACEHUB_API_TOKEN") or os.getenv(
        "huggingfacehub_api_token") or os.getenv("HF_TOKEN")
    if not api_token:
        raise RuntimeError("Missing Hugging Face token. Set HUGGINGFACEHUB_API_TOKEN in your environment or local .env file; never commit the token.")
    endpoint = HuggingFaceEndpoint(repo_id=model_name, max_new_tokens=2048,
                                   temperature=0.2, huggingfacehub_api_token=api_token)
    chat_model = ChatHuggingFace(llm=endpoint)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Create multiple-choice questions strictly from the supplied study text. Return only a valid JSON array. Each object must have question (string), options (array of four strings), answer (exactly one option string), and explanation (string). Do not invent facts not supported by the text."),
        ("human", "Create {count} MCQs from this study text:\n\n{context}"),
    ])
    response = (prompt | chat_model).invoke({"count": num_questions, "context": context.strip()})
    content = response.content if hasattr(response, "content") else str(response)
    return parse_mcqs(content)
