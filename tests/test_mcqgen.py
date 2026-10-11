import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from mcqgen.mcqgenerater import parse_mcqs, generate_mcqs
from mcqgen.utils import read_file

SAMPLE = [{
    "question": "Which gas do plants absorb?",
    "options": ["Oxygen", "Carbon dioxide", "Nitrogen", "Hydrogen"],
    "answer": "Carbon dioxide",
    "explanation": "Plants use carbon dioxide during photosynthesis.",
}]

class ParseMCQTests(unittest.TestCase):
    def test_parse_json_array(self):
        self.assertEqual(parse_mcqs(json.dumps(SAMPLE)), SAMPLE)

    def test_parse_markdown_fence(self):
        fence = chr(96) * 3
        self.assertEqual(parse_mcqs(fence + "json\n" + json.dumps(SAMPLE) + "\n" + fence), SAMPLE)

    def test_reject_invalid_json(self):
        with self.assertRaises(ValueError):
            parse_mcqs("[not valid json]")

    def test_reject_missing_fields(self):
        with self.assertRaises(ValueError):
            parse_mcqs('[{"question":"Q"}]')

class InputHelperTests(unittest.TestCase):
    def test_read_text_path(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "notes.txt"
            path.write_text("study notes", encoding="utf-8")
            self.assertEqual(read_file(path), "study notes")

    def test_read_text_file_object(self):
        stream = io.BytesIO(b"study notes")
        stream.name = "notes.txt"
        self.assertEqual(read_file(stream), "study notes")

    def test_reject_unsupported_extension(self):
        with self.assertRaises(ValueError):
            read_file("notes.docx")

class GenerateMCQTests(unittest.TestCase):
    def test_validates_context_before_model_setup(self):
        with self.assertRaises(ValueError):
            generate_mcqs("  ", token="dummy")

    def test_validates_question_count(self):
        with self.assertRaises(ValueError):
            generate_mcqs("some context", num_questions=0, token="dummy")

    @patch("mcqgen.mcqgenerater.HuggingFaceEndpoint")
    @patch("mcqgen.mcqgenerater.ChatHuggingFace")
    def test_generation_chain_returns_parsed_mcqs(self, mock_chat, mock_endpoint):
        from types import SimpleNamespace
        mock_chat.return_value = object()
        fake_chain = SimpleNamespace(invoke=lambda values: SimpleNamespace(content=json.dumps(SAMPLE)))
        with patch("mcqgen.mcqgenerater.ChatPromptTemplate.from_messages") as prompt_factory:
            prompt_factory.return_value.__or__.return_value = fake_chain
            result = generate_mcqs("plants absorb carbon dioxide", token="dummy")
        self.assertEqual(result, SAMPLE)
        mock_endpoint.assert_called_once()

if __name__ == "__main__":
    unittest.main()
