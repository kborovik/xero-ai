"""AI Agents

This module contains AI agents that perform the following tasks:
    - send invoice to visual LLM and returns the JSON structured data.

"""

import json

from pydantic_ai import Agent

from .schema import Bill

ocr_agent = Agent(
    model="google-gla:gemini-2.0-flash-exp",
    result_type=Bill,
    system_prompt=(
        "You are an AI assistant that helps users to extract information from bills and invoices using visual LLM."
        "You are given a bill and you need to extract the following information:"
        f"{json.dumps(Bill.model_json_schema())}"
        "You need to return the JSON structured data."
    ),
)
