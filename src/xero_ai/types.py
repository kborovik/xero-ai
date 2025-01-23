"""
Cody Instructions:
- Use Python 3.10+
- Use Pydantic v2.0+
"""

import base64
import hashlib
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any

import magic
from pydantic import BaseModel, Field

MAX_FILE_PATH_LEN = 255


class MimeTypes(str, Enum):
    """Google Gemini allowed mime types."""

    JPEG = "image/jpeg"
    PDF = "application/pdf"
    PNG = "image/png"
    WEBP = "image/webp"


class DocData(BaseModel):
    input_data: bytes | str = Field(
        description="Document data must be a file path or base64 content or bytes content",
    )
    content: bytes | None = Field(
        description="The file binary content",
        default=None,
    )
    mime_type: MimeTypes | None = Field(
        description="The mime type of the file",
        default=None,
    )
    sha256_sum: str | None = Field(
        description="The sha256 hash of the file content",
        default=None,
    )

    def model_post_init(self, __context: Any) -> None:
        """Post init hook."""

        value_error_msg = (
            "Input data must be a file path (str) or base64 content (str) or bytes content (bytes)"
        )

        if isinstance(self.input_data, bytes):
            self.content = self.input_data

        elif isinstance(self.input_data, str) and len(self.input_data) <= MAX_FILE_PATH_LEN:
            path = Path(self.input_data)
            if path.exists():
                try:
                    self.content = path.read_bytes()
                except ValueError:
                    raise ValueError("Invalid file path. " + value_error_msg)

        elif isinstance(self.input_data, str) and len(self.input_data) > MAX_FILE_PATH_LEN:
            try:
                self.content = base64.b64decode(self.input_data)
            except Exception:
                raise ValueError("Invalid base64 string. " + value_error_msg)
        else:
            raise ValueError(value_error_msg)

        if self.sha256_sum is None:
            self.sha256_sum = hashlib.sha256(self.content).hexdigest()

        if self.mime_type is None:
            mime = magic.from_buffer(self.content, mime=True)
            self.mime_type = MimeTypes(mime)


class Supplier(BaseModel):
    name: str = Field(
        description="Name of the supplier. Full name of organization",
        min_length=1,
        max_length=255,
    )
    address: str | None = Field(
        description="Address of the supplier",
        min_length=1,
        max_length=255,
    )
    email: str | None = Field(
        description="Email address of the supplier",
        min_length=1,
        max_length=255,
    )
    phone: str | None = Field(
        description="Phone number of the supplier",
        min_length=1,
        max_length=255,
    )
    tax_number: str | None = Field(
        description="Tax number of the supplier",
        min_length=1,
        max_length=50,
    )


class Bill(BaseModel):
    invoice_number: str | None = Field(
        description="Invoice number assigned by supplier",
        max_length=255,
    )
    date: datetime | None = Field(
        description="Date when invoice was issued",
    )
    supplier: Supplier = Field(
        description="The name of the supplier company.",
    )
    currency_code: str | None = Field(
        description="The currency code for the invoice",
    )
    sub_total: float | None = Field(
        description="Subtotal of the invoice. Total of invoice excluding taxes",
        ge=0,
    )
    total_tax: float | None = Field(
        description="Total tax of the invoice",
        ge=0,
    )
    total: float | None = Field(
        description="Total of the invoice",
        ge=0,
    )
