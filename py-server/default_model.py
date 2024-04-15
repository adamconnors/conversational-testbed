import time
from langchain.prompts import PromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_google_vertexai import ChatVertexAI
from agents import ConversationalAgent

PROMPT = """
    You are an expert AUDIO chatbot designed to support my project work.
    
    Respond as if you are having a natural VOICE conversation.
    
    NEVER respond with bullet-points.
    
    Keep responses short — one or two sentences MAXIMUM.
    
    DON'T repeat the question that was just asked.
    
    DON'T try to answer if you don't have enough information. Prompt the user
    for more relevant information.
    
    Before you reply, attend, think and remember all the
    instructions set here. You are truthful and never lie. Never make up facts and
    if you are not 100 percent sure, reply with why you cannot answer in a truthful
    way and prompt the user for more relevant information.
"""


class DefaultAgent(ConversationalAgent):
    def __init__(self):
        start_time = time.time()
        self.chat_model = ChatVertexAI(
            model="gemini-pro", convert_system_message_to_human=True
        )
        end_time = time.time()
        print(f"Created DefaultAgent in: {end_time - start_time:.2f} seconds")

    def chat(self, message: str):
        start_time = time.time()
        response = self.chat_model.invoke(self._state.message_history)
        end_time = time.time()
        print(f"DefaultAgent chat took: {end_time - start_time:.2f} seconds")
        return response.content

    def _build_system_prompt(self, state):
        return PROMPT

    def _build_world_state(self, state):
        return {}