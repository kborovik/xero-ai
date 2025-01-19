"""
Cody Instructions:
- Use Python 3.10+
- Use Pydantic v2.0+
"""

from datetime import datetime

from pydantic import BaseModel, Field


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
    status: str = Field(
        description="The status of the invoice",
        default="DRAFT",
    )
