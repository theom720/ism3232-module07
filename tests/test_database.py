# test_database.py
# Author: Theo Major

import database


def make_db(tmp_path):
    """Create a fresh database with the sample rows, in a folder only this test uses."""
    db_file = tmp_path / "test.db"
    database.create_tables(db_file)
    return db_file


def test_create_tables_twice_adds_no_duplicate_rows(tmp_path):
    db_file = make_db(tmp_path)
    database.create_tables(db_file)
    assert len(database.all_orders(db_file)) == 6
    assert len(database.product_names(db_file)) == 8


def test_find_order_needs_the_exact_id(tmp_path):
    db_file = make_db(tmp_path)
    assert database.find_order(db_file, "K1000") is None
    assert database.find_order(db_file, "k100") is None


def test_sql_in_an_order_id_is_just_text(tmp_path):
    db_file = make_db(tmp_path)
    assert database.find_order(db_file, "K100'; DROP TABLE orders;--") is None
    assert len(database.all_orders(db_file)) == 6


def test_change_requests_get_numbers_and_wait(tmp_path):
    db_file = make_db(tmp_path)
    number = database.add_change_request(db_file, "K100", "9 Pine Street")
    assert number == 1
    assert database.find_request(db_file, 1)["status"] == "waiting"
    assert database.waiting_requests(db_file)[0]["order_id"] == "K100"


def test_approve_changes_the_address_once(tmp_path):
    db_file = make_db(tmp_path)
    database.add_change_request(db_file, "K100", "9 Pine Street")
    assert database.approve_request(db_file, 1) == "Request 1 approved."
    assert database.find_order(db_file, "K100")["address"] == "9 Pine Street"
    assert database.approve_request(db_file, 1) == "Request 1 is already approved."
    assert database.waiting_requests(db_file) == []


def test_reject_changes_nothing_and_cannot_be_approved_later(tmp_path):
    db_file = make_db(tmp_path)
    database.add_change_request(db_file, "K100", "9 Pine Street")
    assert database.reject_request(db_file, 1) == "Request 1 rejected."
    assert database.find_order(db_file, "K100")["address"] == "14 Oak St, Austin TX"
    assert database.approve_request(db_file, 1) == "Request 1 is already rejected."
