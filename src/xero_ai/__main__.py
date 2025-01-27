import argparse

from .gemini import process_bill
from .types import DocData


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="xero-ai",
        description="Process invoices using Google Gemini Vision AI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    invoice_parser = subparsers.add_parser("invoice", help="Process invoice")
    invoice_parser.add_argument(
        "-f",
        "--file",
        type=str,
        help="Path to invoice file (PDF/PNG/JPEG/WEBP)",
    )

    args = parser.parse_args()

    if args.command == "invoice":
        if args.file:
            document = DocData(input_data=args.file)
            bill = process_bill(document)
            print(bill.model_dump_json(indent=2))
        else:
            invoice_parser.print_help()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
