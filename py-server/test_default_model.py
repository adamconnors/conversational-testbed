import json
import unittest
from main import build_message_history
from default_model import DefaultModel
from vertexai.language_models import ChatMessage
from langchain_core.messages import HumanMessage, AIMessage


# Create a test class for the build_message_history function
class TestDefaultModel(unittest.TestCase):

    def setUp(self):
        self.model = DefaultModel()

    def test_build_message_history(self):
        incoming_messages = json.dumps(
            [
                {"content": "Message 1", "author": "user"},
                {"content": "Message 2", "author": "llm"},
                {"content": "Message 3", "author": "user"},
                {"content": "Message 4", "author": "llm"},
            ]
        )

        expected_messages = [
            ChatMessage("Message 1", "user"),
            ChatMessage("Message 2", "llm"),
            ChatMessage("Message 3", "user"),
            ChatMessage("Message 4", "llm"),
        ]

        message_history = build_message_history(incoming_messages)
        vertex_message_history = self.model.convert_message_history(message_history)
        self.assertEqual(vertex_message_history, expected_messages)


if __name__ == "__main__":
    unittest.main()
