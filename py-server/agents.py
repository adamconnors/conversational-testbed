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

    def _from_messages(self, system_prompt: str, state: AgentState):
        """
        Builds the prompt template value from the agent's state.
        Equivalent to ChatPromptTemplate.from_messages but adds
        the current message and the system prompt to the message history.
        Args:
            system_prompt: the system prompt for this agent
            state: current agent state
        Returns:
            ChatPromptValue object.
        """
        messages = state.message_history
        messages.insert(0, ("system", system_prompt))
        messages.append(HumanMessage(state.message))
        return ChatPromptTemplate.from_messages(messages)
