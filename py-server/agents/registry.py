from typing import Dict, Final
from .agents import ConversationalAgent
from .default_agent import DefaultAgent
from .fake_agent import FakeAgent
from .history_tutor.history_tutor import HistoryTutor

# Create conversational agents. An agent is a ConversationalAgent subclass.
# It's able to respond to user messages based on the conversation history
# and previous state.
# New agents should be registered here.
AGENT_BY_ID: Final[Dict[str, ConversationalAgent]] = {
    "default": DefaultAgent(),
    "fake": FakeAgent(),
    "history_tutor": HistoryTutor(),
}
