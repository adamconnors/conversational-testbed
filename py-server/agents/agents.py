from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Any, List, Tuple
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate


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

    @abstractmethod
    def chat(self, agent_state: AgentState) -> AgentResponse:
        """Handles a single message exchange with the conversational agent.

        Args:
            message: incoming user message.
        Returns:
            The agent's response message.
        """
        pass

    def get_system_prompt(self) -> str:
        """Returns the main (conversational) system prompt for the agent.
        This is only needed in order to use interactive alignment tools.
        """
        return None
