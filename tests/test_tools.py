# test_tools.py
# Author: Theo Major

import database
from tools import KoreTools


def make_tools(tmp_path):
    """Build tools over a fresh database with the sample rows."""
    db_file = tmp_path / "test.db"
    database.create_tables(db_file)
    return KoreTools(db_file)


def customer(text):
    """Build a history that holds one customer message."""
    return [{"role": "user", "content": text}]


def test_look_up_order_finds_the_id_inside_a_sentence(tmp_path):
    tools = make_tools(tmp_path)
    reply = tools.run(
        "look_up_order", {"order_id": "where is K100?"}, customer("where is K100?")
    )
    assert reply == "Order K100 is shipped."


def test_request_address_change_files_and_waits(tmp_path):
    tools = make_tools(tmp_path)
    history = customer("change order K101 to 9 Pine Street")
    reply = tools.run(
        "request_address_change",
        {"order_id": "K101", "new_address": "9 Pine Street"},
        history,
    )
    assert "sent to staff" in reply
    assert database.waiting_requests(tools.db_file)[0]["order_id"] == "K101"


def test_unknown_tool_is_refused(tmp_path):
    tools = make_tools(tmp_path)
    reply = tools.run("delete_everything", {}, customer("hi"))
    assert reply == "There is no tool named delete_everything."


def test_missing_order_id_is_refused(tmp_path):
    tools = make_tools(tmp_path)
    reply = tools.run("look_up_order", {}, customer("where is my order?"))
    assert "missing" in reply


def test_made_up_order_id_is_refused(tmp_path):
    tools = make_tools(tmp_path)
    reply = tools.run("look_up_order", {"order_id": "K101"}, customer("Where is K100?"))
    assert "has not given that order ID" in reply


def test_typo_order_id_does_not_count_as_typed(tmp_path):
    tools = make_tools(tmp_path)
    history = customer("Change order K1000 to 9 Pine Street")
    lookup = tools.run("look_up_order", {"order_id": "K100"}, history)
    assert "has not given that order ID" in lookup
