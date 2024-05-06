import time
from langchain_google_vertexai import ChatVertexAI
from agents import AgentResponse, ConversationalAgent

SYSTEM_PROMPT = """
    You are an expert chatbot designed to help me.
    
    Respond as if you are having a natural VOICE conversation.
    
    NEVER respond with bullet-points.
    
    Keep responses short — one or two sentences MAXIMUM.
    
    DON'T repeat the question that was just asked.
    
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
        self.chat_model = ChatVertexAI(
            model="gemini-pro", convert_system_message_to_human=False
        )

    def chat(self, agent_state) -> AgentResponse:
        promptTemplate = self._from_messages(SYSTEM_PROMPT, agent_state)
        prompt = promptTemplate.invoke({"current_time": time.strftime("%I:%M %p")})

        # Invoke the model with the prompt.
        response = self.chat_model.invoke(prompt)
        return (response.content, {})
