"""Google Gemini AI agents

This module contains AI agents that perform the following tasks:
    - send invoice to visual LLM and returns the JSON structured data.

"""

import json

import logfire

from google import genai
from google.genai.types import (
    GenerateContentConfig,
    GenerateContentResponse,
    Part,
)

from .settings import GEMINI_API_KEY, GEMINI_MODEL
from .types import Bill, DocData


def process_bill(document: DocData) -> Bill:
    """Process document and return structured data."""
    bill_schema = json.dumps(Bill.model_json_schema())

    client = genai.Client(api_key=GEMINI_API_KEY)

    logfire.info(f"Processing document: {document.sha256_sum}")

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

    try:
        bill = Bill.model_validate_json(json_data=response.text, strict=False)
        logfire.info(f"Processed document: {document.sha256_sum}, Invoice Number: {bill.invoice_number}, Supplier: {bill.supplier.name}")
        return bill
    except Exception as e:
        logfire.error(f"Error processing document: {document.sha256_sum}, Error: {e}")
        raise e


if __name__ == "__main__":
    pass
