import base64
from pathlib import Path

from xero_ai.gemini import process_bill
from xero_ai.types import Bill, DocData, Supplier

TEST_FILE = "tests/INV-2878.pdf"
TEST_SHA256 = "3069cf85a04ec21966b93c541bd02985e82a8953222ac948914d8443b7fb7b9a"
TEST_BILL = Bill(
    invoice_number="INV-2878",
    date="2025-01-26T00:00:00",
    supplier=Supplier(
        name="Aerodynamic Frontier Technologies",
        address="1234 Innovation Drive, Suite 450\nVancouver, British Columbia V6C 2T6",
        email="contact@aerodynamicfrontier.com",
        phone="+1 (604) 555-7890",
        tax_number=None,
    ),
    currency_code="CAD",
    sub_total=2209.88,
    total_tax=287.28,
    total=2497.16,
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


def test_doc_data_pdf():
    doc_data_pdf(
        file_path=TEST_FILE,
        sha256_sum=TEST_SHA256,
    )


def test_doc_data_base64():
    doc_data_base64(
        file_path=TEST_FILE,
        sha256_sum=TEST_SHA256,
    )


def test_process_bill():
    document = DocData(input_data=TEST_FILE)
    bill = process_bill(document)
    assert bill == TEST_BILL, "Values of object Bill should be equal to test data"
