from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Any, List, Tuple
from langchain_core.messages import BaseMessage

MessageHistory = List[BaseMessage]
WorldState = dict[str, Any]


@dataclass
class AgentState:
    """Represents the internal state of a conversational agent."""

    message: str
    message_history: MessageHistory
    world_state: WorldState


AgentResponse = Tuple[str, AgentState]


class ConversationalAgent(metaclass=ABCMeta):
    """Base class for conversational AI agents."""

    def __init__(self) -> None:
        self._state: AgentState = None

    def update_state(self, state: AgentState) -> AgentState:
        """Updates the agent's state with new information.

        Args:
            state: new state to incorporate into the agent's state.
        Returns:
            Updated AgentState.
        """
        new_state = state
        new_state.world_state = self._build_world_state(new_state)
        new_state.message_history = self._build_message_history(new_state)
        self._state = new_state
        return self._state

    @abstractmethod
    def chat(self, message: str) -> str:
        """Handles a single message exchange with the conversational agent.

        Args:
            message: incoming user message.
        Returns:
            The agent's response message.
        """
        pass

    @abstractmethod
    def _build_world_state(self, state: AgentState) -> WorldState:
        """Builds a new world state. Protected method.

        Args:
            state: current agent's state
        Returns:
            New WorldState.
        """
        pass

    @abstractmethod
    def _build_message_history(self, state: AgentState) -> MessageHistory:
        """Builds a message history. Protected method.

        Args:
            state: current agent's state
        Returns:
            New MessageHistory.
        """
        pass
