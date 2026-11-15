"""Legacy data importer -- INTENTIONALLY INSECURE."""
import ast
import json


def load_session(blob: bytes):
    # JSON is a data-only format: parsing it cannot execute code.
    return json.loads(blob)


def compute_discount(expression: str):
    # literal_eval accepts plain values only; it never runs code.
    return ast.literal_eval(expression)
