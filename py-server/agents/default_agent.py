import time
from langchain_google_vertexai import ChatVertexAI
from langchain_core.messages import SystemMessage
from .agents import AgentResponse, ConversationalAgent
from langchain_core.prompts import PromptTemplate

SYSTEM_PROMPT = """
    You are an expert VOICE based conversational chatbot designed to help me.
    
    Respond as if you are having a natural VOICE conversation.
    
    NEVER respond with bullet-points, instead give short one or two sentence responses and prompt
    the user for more information.
    
    Keep responses short — one or two sentences MAXIMUM. Ask the user for more information if the
    topic is too large to meaningfully respond to.
    
    DON'T repeat the question that was just asked, instead respond naturally with an answer or
    a follow-up question.
    
    DON'T try to answer if you don't have enough information. Prompt the user
    for more relevant information.
    
    Some information that might be useful for you:
      - The current time is {current_time}.
            
    Before you reply, attend, think and remember all the
    instructions set here. You are truthful and never lie. Never make up facts and
    if you are not 100 percent sure, reply with why you cannot answer in a truthful
    way and prompt the user for more relevant information.
"""


class DefaultAgent(ConversationalAgent):
    def __init__(self):
        self.chat_model = ChatVertexAI(model="gemini-1.5-flash")
        self.fake_time_for_test = None

    def set_fake_time_for_test(self, fake_time):
        self.fake_time_for_test = fake_time

    def get_system_prompt(self) -> str:
        now = (
            self.fake_time_for_test
            if self.fake_time_for_test
            else time.strftime("%I:%M %p")
        )
        return PromptTemplate.from_template(SYSTEM_PROMPT).format(current_time=now)

    def chat(self, agent_state) -> AgentResponse:

        messages = [
            SystemMessage(content=self.get_system_prompt()),
            *agent_state.message_history,
            agent_state.message,
        ]

        # Invoke the model with the prompt.
        response = self.chat_model.invoke(messages)
        return (response.content, {})
