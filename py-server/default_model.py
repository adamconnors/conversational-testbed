from vertexai.language_models import ChatMessage, ChatModel
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
import time

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


class DefaultModel:
    def __init__(self):

        start_time = time.time()
        self.chat_model = ChatModel.from_pretrained("chat-bison@002")
        end_time = time.time()
        print(f"Created DefaultModel in: {end_time - start_time:.2f} seconds")

    def chat(self, message_history, world_state, message):
        start_time = time.time()
        messages = self.convert_message_history(message_history)
        chat_session = self.chat_model.start_chat(
            context=PROMPT, message_history=messages
        )
        res = chat_session.send_message(message)
        end_time = time.time()
        print(f"DefaultModel chat took: {end_time - start_time:.2f} seconds")
        text = res.candidates[0].text
        return text, None

    def convert_message_history(self, message_history):
        """
        Converts langchain message history to ChatMessage format
        so that we can always refer back to the direct API version.
        """
        messages = []
        for message in message_history:
            if isinstance(message, AIMessage):
                messages.append(ChatMessage(content=message.content, author="llm"))
            elif isinstance(message, HumanMessage):
                messages.append(ChatMessage(content=message.content, author="user"))
        if not message_history:
            message_history = None
        return messages
