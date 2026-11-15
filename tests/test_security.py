"""Security regression tests for Part C."""
import sqlite3

import pytest

from tdd_lab.accounts import add_user, find_user, init_db


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