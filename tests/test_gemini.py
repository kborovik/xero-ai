import base64
from pathlib import Path

import pytest

from xero_ai.gemini import create_bill
from xero_ai.types import Bill, DocData, Supplier

bill1 = Bill(
    invoice_number="5142408989",
    date="2024-12-31T00:00:00",
    supplier=Supplier(
        name="Google LLC",
        address="1600 Amphitheatre Pkwy\nMountain View, CA 94043\nUnited States",
        email=None,
        phone=None,
        tax_number="852407436 RT9999",
    ),
    currency_code="CAD",
    sub_total=22.03,
    total_tax=0.0,
    total=22.03,
)


bill2 = Bill(
    invoice_number="8642EB5C-0002",
    date="2025-01-20T00:00:00",
    supplier=Supplier(
        name="Midjourney Inc",
        address="611 Gateway Blvd\nSuite 120\nSouth San Francisco, California 94080\nUnited States",
        email="billing@midjourney.com",
        phone=None,
        tax_number="791262355RT9999",
    ),
    currency_code="USD",
    sub_total=10.0,
    total_tax=1.3,
    total=11.3,
)


def doc_data_pdf(file_path: str, sha256_sum: str) -> None:
    document = DocData(input_data=file_path)
    assert document.mime_type == "application/pdf", "Mime type should be application/pdf"
    assert document.sha256_sum == sha256_sum, "Sha256 sum should be correct"


def doc_data_base64(file_path: str, sha256_sum: str) -> None:
    content = Path(file_path).read_bytes()
    base64_string = base64.b64encode(content).decode("utf-8")
    document = DocData(input_data=base64_string)
    assert document.mime_type == "application/pdf", "Mime type should be application/pdf"
    assert document.sha256_sum == sha256_sum, "Sha256 sum should be correct"


def test_doc_data_pdf_1():
    doc_data_pdf(
        file_path="tests/invoice1.pdf",
        sha256_sum="5525ab3992594ce8d5723f15dac57cda2d9f1dc0f8e1ac232f6a213d777f8489",
    )


def test_doc_data_base64_1():
    doc_data_base64(
        file_path="tests/invoice1.pdf",
        sha256_sum="5525ab3992594ce8d5723f15dac57cda2d9f1dc0f8e1ac232f6a213d777f8489",
    )


def test_create_bill_1():
    document = DocData(input_data="tests/invoice1.pdf")
    bill = create_bill(document)
    assert bill == bill1, "Values of object Bill should be equal to test data"


def test_doc_data_pdf_2():
    doc_data_pdf(
        file_path="tests/invoice2.pdf",
        sha256_sum="1be13bc8f2bd08352fc63922ea4ae4a10480f3085d126b01f1e64d2d9c676ae0",
    )


def test_doc_data_base64_2():
    doc_data_base64(
        file_path="tests/invoice2.pdf",
        sha256_sum="1be13bc8f2bd08352fc63922ea4ae4a10480f3085d126b01f1e64d2d9c676ae0",
    )


def test_create_bill_2():
    document = DocData(input_data="tests/invoice2.pdf")
    bill = create_bill(document)
    assert bill == bill2, "Values of object Bill should be equal to test data"
