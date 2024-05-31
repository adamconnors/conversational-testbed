import unittest
from fake_agent import FakeAgent
import test_utils
from agents import AgentResponse, AgentState


class TestFakeAgent(unittest.TestCase):
    def test_chat(self):
        agent = FakeAgent()
        message_history = test_utils.build_message_history_for_test([])
        response, world_state = agent.chat(AgentState("Hello", message_history, None))
        self.assertEqual(response, "Fake response to message 0: Hello")
        self.assertEqual(world_state, {"last_message": "Hello", "message_count": 0})

        message_history = test_utils.build_message_history_for_test(
            ["Hello", response, "How are you?"]
        )
        response, world_state = agent.chat(
            AgentState("How are you?", message_history, world_state)
        )
        self.assertEqual(response, "Fake response to message 3: How are you?")
        self.assertEqual(
            world_state, {"last_message": "How are you?", "message_count": 3}
        )


if __name__ == "__main__":
    unittest.main()
