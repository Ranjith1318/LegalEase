import os
import re

from dotenv import load_dotenv
from google import genai

load_dotenv()


class GeminiDocumentGenerator:

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

        if not api_key or api_key == "PASTE_YOUR_GEMINI_API_KEY_HERE":
            raise ValueError(
                "GEMINI_API_KEY is missing. Please add your Gemini API key to .env"
            )

        self.client = genai.Client(api_key=api_key)
        self.model = model

    def generate(self, document_type, parties, terms, effective_date,
                 jurisdiction="India", instructions=""):

        prompt = f"""
You are a professional legal document drafting assistant.

Create a clear and professionally structured draft legal document.

Document Type:
{document_type}

Parties:
{parties}

Key Terms:
{terms}

Effective Date:
{effective_date}

Jurisdiction:
{jurisdiction}

Additional Instructions:
{instructions}

Requirements:
1. Create a professional legal document.
2. Use clear section headings.
3. Include the parties and effective date.
4. Include the provided key terms.
5. Use numbered clauses where appropriate.
6. Add standard clauses relevant to the document type.
7. Do not invent specific personal information.
8. Clearly indicate placeholders where information is missing.
9. Return only the document draft.
10. Include a short disclaimer at the end that the document should be reviewed by a qualified legal professional before use.

This is a drafting assistant and not a substitute for professional legal advice.
"""

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )

        text = response.text or ""

        # Normalize some problematic typography.
        text = text.replace("—", "-")
        text = text.replace("–", "-")
        text = text.replace("“", '"')
        text = text.replace("”", '"')
        text = text.replace("’", "'")

        # Remove accidental excessive blank lines.
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text.strip()