import json
import unittest
from langchain_core.messages import AIMessage, HumanMessage
from history_tutor import HistoryTutor
from agents import AgentState


class TestHistoryTutor(unittest.TestCase):
    def setUp(self):
        print("\n\n------")
        self.agent_state = AgentState("hello", [], {})
        self.tutor = HistoryTutor()

    def test_start_lesson(self):
        self.send_message("start lesson")
        self.send_message("was it god?")
        self.send_message("what about miasma and bad smells")
        self.send_message("prayer")
        json_str = json.dumps(self.agent_state, indent=4)
        print(json_str)

    # @unittest.skip("skipping")
    def test_create_initial_world_state(self):
        state = self.tutor.update_state(self.agent_state)
        json_str = json.dumps(state.world_state, indent=4)
        print(json_str)

    # @unittest.skip("skipping")
    def test_update_world_state(self):
        next_state = self.tutor.update_state(self.agent_state)
        latest_response = """
          AI: What did people believe caused the Black Death?
          User: Religion: God sent the plague as a punishment for people's sins.
          AI: What other examples can you think of?
          User: Miasma?
        """
        updated_state = self.tutor.update_state(next_state)
        json_str = json.dumps(updated_state.world_state, indent=4)
        print(json_str)

    def send_message(self, message):
        self.agent_state = self.tutor.update_state(self.agent_state)
        response = self.tutor.chat(message)
        print(f"user: ${message}\nAI: ${response}")
        # remove the system prompt from the message history
        self.agent_state.message_history = self.agent_state.message_history[1:]
        return response


if __name__ == "__main__":
    unittest.main()