"""Legacy account helpers -- INTENTIONALLY INSECURE. Your job: scan, triage, fix.

Every weakness below is something a real static-analysis tool will flag.
"""
import hashlib
import hmac
import os
import sqlite3

SECRET_KEY = os.environ.get("APP_SECRET_KEY", "")

PBKDF2_ITERATIONS = 600_000


def hash_password(password: str) -> str:
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        PBKDF2_ITERATIONS,
    )
    return salt.hex() + "$" + digest.hex()


def verify_password(password: str, stored: str) -> bool:
    salt_hex, digest_hex = stored.split("$")
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        bytes.fromhex(salt_hex),
        PBKDF2_ITERATIONS,
    )
    return hmac.compare_digest(digest.hex(), digest_hex)


def init_db(conn: sqlite3.Connection) -> None:
    conn.execute("CREATE TABLE IF NOT EXISTS users (name TEXT, pw_hash TEXT)")
    conn.commit()


def add_user(conn: sqlite3.Connection, name: str, password: str) -> None:
    conn.execute(
        "INSERT INTO users (name, pw_hash) VALUES (?, ?)",
        (name, hash_password(password)),
    )
    conn.commit()


def find_user(conn: sqlite3.Connection, name: str):
    return conn.execute(
        "SELECT name, pw_hash FROM users WHERE name = ?", (name,)
    ).fetchone()


def check_login(conn: sqlite3.Connection, name: str, password: str) -> bool:
    row = find_user(conn, name)
    return row is not None and verify_password(password, row[1])
