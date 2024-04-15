import unittest
from history_tutor import HistoryTutor
from langchain_core.messages import AIMessage, HumanMessage
import json
from tabulate import tabulate


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
        self.dump_world_state(self.world_state)
        
    @unittest.skip("skipping")
    def test_create_initial_world_state(self):
        state = self.tutor.build_world_state()
        json_str = json.dumps(state, indent=4)
        print(json_str)

    @unittest.skip("skipping")
    def test_update_world_state(self):
        state = self.tutor.build_world_state()
        self.dump_world_state(state)
        
        
        chat_history = """
        [HumanMessage(content='start lesson'), 
        AIMessage(content="Let's begin with the first question. What were the different theories about the cause of the Black Death?")]
        """ 
        
        latest_response = """Was it god?"""
        
        new_state = self.tutor.update_world_state(state, chat_history, latest_response)
        self.dump_world_state(new_state)

    
    def dump_world_state(self, world_state):
        json_str = json.dumps(world_state, indent=4)
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
