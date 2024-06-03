from .agents import AgentResponse, ConversationalAgent


class FakeAgent(ConversationalAgent):
    """Fake agent for testing that always returns a canned response and world_state."""

    def chat(self, agent_state) -> AgentResponse:
        message_count = len(agent_state.message_history)
        message = agent_state.message
        world_state = agent_state.world_state
        print(world_state)
        if world_state == None:
            world_state = self._create_initial_world_state(message, message_count)
        else:
            world_state["last_message"] = message
            world_state["message_count"] = message_count

        return (f"Fake response to message {message_count}: {message}", world_state)

    def _create_initial_world_state(self, last_message, message_count):
        return {
            "last_message": last_message,
            "message_count": message_count,
        }
