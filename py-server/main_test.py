import json
import unittest
from main import build_message_history
from langchain_core.messages import HumanMessage, AIMessage


# Create a test class for the build_message_history function
class TestMain(unittest.TestCase):
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
            HumanMessage("Message 1"),
            AIMessage("Message 2"),
            HumanMessage("Message 3"),
            AIMessage("Message 4"),
        ]
        output = build_message_history(incoming_messages)
        self.assertEqual(output, expected_messages)


    def test_invalid_history(self):
        incoming_messages = "xxx"
        try:
            output = build_message_history(incoming_messages)
            self.fail("Should have thrown an exception")
        except Exception as e:
            pass

if __name__ == "__main__":
    unittest.main()
