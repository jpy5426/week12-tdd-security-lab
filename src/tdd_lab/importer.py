"""Legacy data importer -- INTENTIONALLY INSECURE."""
import json


def load_session(blob: bytes):
    # JSON is a data-only format: parsing it cannot execute code.
    return json.loads(blob)


def compute_discount(expression: str):
    # "Flexible" pricing rules typed in by an admin.
    return eval(expression)