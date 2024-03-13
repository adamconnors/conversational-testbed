from vertexai.language_models import ChatMessage, ChatModel

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
        self.chat_model = ChatModel.from_pretrained("chat-bison@002")
    
    def chat(self, message_history, message):
        chat_session = self.chat_model.start_chat(
            context=PROMPT, message_history=message_history
        )
        res = chat_session.send_message(message)
        text = res.candidates[0].text
        return text
