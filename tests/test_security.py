"""Security regression tests for Part C."""
import sqlite3

import pytest

from tdd_lab.accounts import add_user, find_user, init_db
from tdd_lab import exporter
from tdd_lab.importer import compute_discount, load_session

@pytest.fixture
def conn():
    connection = sqlite3.connect(":memory:")
    init_db(connection)
    yield connection
    connection.close()


def test_find_user_blocks_sql_injection(conn):
    add_user(conn, "ada", "s3cret!")
    assert find_user(conn, "x' OR '1'='1") is None


def test_same_password_gets_different_hashes(conn):
    add_user(conn, "ada", "s3cret!")
    add_user(conn, "bob", "s3cret!")
    assert find_user(conn, "ada")[1] != find_user(conn, "bob")[1]


def test_archive_report_does_not_use_shell(monkeypatch):
    calls = []

    def fake_call(args, **kwargs):
        calls.append((args, kwargs))
        return 0

    monkeypatch.setattr(exporter.subprocess, "call", fake_call)
    hostile = "report.csv; echo hacked"
    exporter.archive_report(hostile)
    args, kwargs = calls[0]
    assert args == ["zip", "-q", "archive.zip", "--", hostile]
    assert not kwargs.get("shell")


def test_load_session_reads_json():
    assert load_session(b'{"user": "ada"}') == {"user": "ada"}