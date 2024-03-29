import json
import unittest
from main import build_message_history
from langchain_core.messages import HumanMessage, AIMessage
from main import app


# Create a test class for the build_message_history function
class TestMain(unittest.TestCase):

    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self):
        self.ctx.pop()

    def test_no_world_state(self):
        req = {
            "q": "user message",
            "mode": "fake",
        }
        resp = self.client.post("/chat", data=req)
        data = json.loads(resp.get_data())
        self.assertEqual(data["response"], "This is a canned response.")
        self.assertEqual(data["world_state"][0]["user"], "user message")

    def test_world_state_round_trip(self):
        req = {
            "q": "user message 1",
            "mode": "fake",
            "worldstate": "[]",
        }
        resp = self.client.post("/chat", data=req)
        data = json.loads(resp.get_data())
        world_state = data["world_state"]

        next_req = {
            "q": "user message 2",
            "mode": "fake",
            "world_state": json.dumps(world_state),
        }

        resp2 = self.client.post("/chat", data=next_req)
        data2 = json.loads(resp2.get_data())
        world_state2 = data2["world_state"]
        self.assertEqual(world_state2[0]["user"], "user message 1")
        self.assertEqual(world_state2[1]["user"], "user message 2")

    @unittest.skip("Not implemented")
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
