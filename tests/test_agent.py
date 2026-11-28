# test_agent.py
# Author: Theo Major

import database
from agent import SupportChatbot
from fake_model import FakeModel
from fallback_model import FallbackModel
from keyword_model import KeywordModel
from tools import KoreTools


class SilentModel:
    """A model that never has an answer. It stands in for Ollama being switched off."""

    def decide(self, instructions, history, tools):
        return None


def make_bot(tmp_path, model):
    """Build a chatbot over a fresh database with the sample rows."""
    db_file = tmp_path / "test.db"
    database.create_tables(db_file)
    return SupportChatbot("Sunny", "Be friendly.", KoreTools(db_file), model)


def ask_for_tool(name, arguments):
    """Build the decision a model returns when it wants a tool."""
    return {"tool": name, "arguments": arguments}


def test_model_chosen_lookup_answers_from_the_database(tmp_path):
    model = FakeModel(
        [
            ask_for_tool("look_up_order", {"order_id": "K101"}),
            {"text": "Your order K101 is still processing."},
        ]
    )
    bot = make_bot(tmp_path, model)
    bot.respond("Has my order K101 shipped?")
    assert bot.history[1]["content"] == "Order K101 is processing."


def test_made_up_address_never_reaches_the_database(tmp_path):
    model = FakeModel(
        [
            ask_for_tool(
                "request_address_change",
                {"order_id": "K102", "new_address": "123 Main St"},
            ),
            {"text": "What is the new address?"},
        ]
    )
    bot = make_bot(tmp_path, model)
    bot.respond("Please change the address on order K102")
    assert database.waiting_requests(bot.tools.db_file) == []


def test_fallback_uses_keyword_model_when_ollama_is_silent(tmp_path):
    model = FallbackModel(SilentModel(), KeywordModel())
    bot = make_bot(tmp_path, model)
    reply = bot.respond("Where is order K100?")
    assert reply == "Order K100 is shipped."
