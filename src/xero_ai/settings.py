import os

import dotenv

# import google.auth

dotenv.load_dotenv()

# GOOGLE_CREDENTIALS, GOOGLE_PROJECT_ID = google.auth.default()

# POSTGRES_HOST = os.environ.get("POSTGRES_HOST", default="localhost")
# POSTGRES_PORT = os.environ.get("POSTGRES_PORT", default="5432")
# POSTGRES_DB = os.environ.get("POSTGRES_DB", default="invoice_ocr")
# POSTGRES_USER = os.environ.get("POSTGRES_USER", default="postgres")
# POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", default="postgres")

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-2.0-flash-exp"

LOGFIRE_SERVICE_NAME = os.environ.get("LOGFIRE_SERVICE_NAME", default="xero-ai")
