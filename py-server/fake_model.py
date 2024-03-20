# TODO: Add a base class for a common interface for all models
class FakeModel:
    def chat(self, message_history, world_state, message):
        print(f"Fake called with world state {world_state}")
        if not world_state:
            world_state = [{"user": message}]
        else:
            world_state.append({"user": message})

        return "This is a canned response.", world_state
