from agents import ConversationalAgent


class FakeAgent(ConversationalAgent):
    def chat(self, message):
        print(f"Fake called with world state {self._state.world_state}")
        return "This is a canned response."

    def _build_message_history(self, state):
        return state.message_history

    def _build_world_state(self, state):
        world_state = state.world_state
        if not world_state:
            world_state = {"user_messages": [state.message]}
        else:
            world_state['user_messages'].append(state.message)

        return world_state
