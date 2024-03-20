import unittest
from history_tutor import HistoryTutor
from langchain_core.messages import AIMessage, HumanMessage
from tabulate import tabulate
import json


class TestHistoryTutor(unittest.TestCase):
    def setUp(self):
        print("\n\n------")
        self.message_history = []
        self.tutor = HistoryTutor()
        self.world_state = self.tutor.build_world_state()

    def test_start_lesson(self):
        self.send_message("start lesson")
        self.send_message("was it god?")
        self.send_message("what about miasma and bad smells")
        self.send_message("prayer")
        json_str = json.dumps(self.world_state, indent=4)
        print(json_str)

    @unittest.skip("skipping")
    def test_create_initial_world_state(self):
        state = self.tutor.build_world_state()
        json_str = json.dumps(state, indent=4)
        print(json_str)

    @unittest.skip("skipping")
    def test_update_world_state(self):
        state = self.tutor.build_world_state()
        latest_response = """
          AI: What did people believe caused the Black Death?
          User: Religion: God sent the plague as a punishment for people's sins.
          AI: What other examples can you think of?
          User: Miasma?
        """
        updated_state = self.tutor.update_world_state(state, latest_response)

        json_str = json.dumps(updated_state, indent=4)
        print(json_str)

    def send_message(self, message):
        response, updated_world_state = self.tutor.chat(
            self.message_history, self.world_state, message
        )
        self.world_state = updated_world_state

        # Updates our message history.
        self.message_history.append(HumanMessage(message))
        self.message_history.append(AIMessage(response))

        print(
            tabulate(
                [
                    [f"User:", f" {message}"],
                    [f"AI:", f"{response}"],
                ],
                tablefmt="grid",
            )
        )

        return response, updated_world_state


if __name__ == "__main__":
    unittest.main()
