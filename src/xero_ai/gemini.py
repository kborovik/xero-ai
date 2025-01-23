"""Google Gemini AI agents

This module contains AI agents that perform the following tasks:
    - send invoice to visual LLM and returns the JSON structured data.

"""

import json

from google import genai
from google.genai.types import (
    GenerateContentConfig,
    GenerateContentResponse,
    Part,
)

from .settings import GEMINI_API_KEY, GEMINI_MODEL
from .types import Bill, DocData


def create_bill(document: DocData) -> Bill:
    """Process invoice and return structured data."""
    bill_schema = json.dumps(Bill.model_json_schema())

    client = genai.Client(api_key=GEMINI_API_KEY)

    response: GenerateContentResponse = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=[
            Part.from_text(f"Extract information according to the schema: {bill_schema}"),
            Part.from_bytes(data=document.content, mime_type=document.mime_type),
        ],
        config=GenerateContentConfig(
            temperature=0.3,
            response_mime_type="application/json",
        ),
    )

    bill = Bill.model_validate_json(json_data=response.text, strict=True)

    return bill


if __name__ == "__main__":
    document = DocData(input_data="data/invoice2.pdf")
    print(document.mime_type)
    print(document.sha256_sum)
    bill = create_bill(document)
    print(bill.model_dump_json(indent=2))
