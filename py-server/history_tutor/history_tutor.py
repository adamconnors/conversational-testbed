import time
from langchain_google_vertexai import ChatVertexAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_core.output_parsers import JsonOutputParser
import json
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage

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


class HistoryTutor:
    def __init__(self):
        start = time.time()
        self.chat_model = ChatVertexAI(
            model="gemini-pro", convert_system_message_to_human=True
        )
        end = time.time()
        print(f"HistoryTutor loaded in {end - start:0.2f} seconds")

    def chat(self, message_history, message):
        print(message_history, message)
        messages = [SystemMessage(PROMPT)]
        messages.extend(message_history)
        messages.append(HumanMessage(message))
        response = self.chat_model.invoke(messages)
        return response.content

    def load_file(filename):
        with open(filename, "r") as file:
            return file.read()

        history_tutor_context = prompts.CONTEXT_HISTORY_TUTOR
        lister_and_carbolic_acid_context = load_file(
            "./history_tutor/lister_and_carbolic_acid.md"
        )
        history_tutor_context = history_tutor_context.replace(
            "%%CONTEXT%%", lister_and_carbolic_acid_context
        )
