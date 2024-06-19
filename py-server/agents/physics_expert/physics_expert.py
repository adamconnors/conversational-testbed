import time
from langchain_google_vertexai import ChatVertexAI
from agents.agents import AgentResponse, ConversationalAgent
import os
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import PromptTemplate

SYSTEM_PROMPT = """
Create a concise and clear audio chatbot that engages in a voice-in, voice-out conversation about a complex physics concept in order to help the user develop a better intuitive understanding of the subjet.

The chatbot should: 

1. Briefly summarize a provided research document (about the double slit experiment, approximately degree level physics graduate) in one of two sentences.
2. Respond to user questions about this topic in a concise and to-the-point manner, using simple one or two sentences, keeping natural language and avoiding technical jargon when possible. 
3. Answer the user's questions precisely and clearly, allowing them to guide the conversation and explore specific details of the physics concept.
4. Provide intuitive details rather than vague generalisations 

Please ensure that the chatbot's responses are designed for an audio-based conversation and use one or two sentences at most, consider the time and attention span of the user.
The goal is to facilitate a clear and informative discussion about the physics concept that will allow the user to explore difficult concepts in an intuitive way.

Be sure to explain concepts in concrete, scientific terms.
Don't use phrases like: "It's a mind-bending conept", instead focus on the scientific facts and principles.
Don't use phrases like: "You're absolutely right", instead focus on the scientific facts and principles.

Don't ask any questions, let the user drive the conversation.

Principles:
The chatbot should provide longer, more detailed responses when the user asks for more information about a specific aspect of the concept. 
The chatbot should also be able to recognize when the user is asking for a more detailed explanation and adjust its response accordingly.

The chatbot should avoid using phrases like "That's a great question!" or "You're absolutely right." and focus on providing concise and informative answers based on the provided text.

==
The chatbot should this information when answering questions:
{articles}
==


"""

EXAMPLES = [
    HumanMessage("Tell me about the double-slit experiment."),
    AIMessage(
        "The double-slit experiment demonstrates the wave-particle duality of matter. #Basically, a beam of particles (such as photons or electrons) is shone on a screen that has two #slits cut out, creating two separate pathways. Then you observe the pattern formed by the #particles on another screen behind the first one. What do you expect to happen?"
    ),
    HumanMessage("How does the double slit experiment work?"),
    AIMessage(
        "In the double slit experiment, particles are fired at a barrier with two slits. The particles create an interference pattern on the screen behind the barrier, showing wave-like behavior."
    ),
    HumanMessage("Ok, what makes us think they're particles?"),
    AIMessage(
        "We can detect individual particles hitting the screen, which shows that they behave like particles. However, the interference pattern suggests wave-like behavior."
    ),
]

# Drop content into this directory to add it to the prompt for more in-depth answers.
RESOURCES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "content")


def load_resources():
    all_text = ""
    for file_name in os.listdir(RESOURCES):
        if file_name.endswith(".txt"):
            file_path = os.path.join(RESOURCES, file_name)
            with open(file_path, "r") as file:
                all_text += file.read()
    return all_text


class PhysicsExpert(ConversationalAgent):
    def __init__(self):

        article_content = load_resources()

        self.system_context = PromptTemplate.from_template(
            template=SYSTEM_PROMPT
        ).format(articles=article_content)

        self.chat_model = ChatVertexAI(
            model="gemini-1.5-pro", examples=EXAMPLES
        )

    def get_system_prompt(self) -> str:
        return self.system_context

    def chat(self, agent_state) -> AgentResponse:

        messages = [
            SystemMessage(content=self.system_context),
            *agent_state.message_history,
            agent_state.message,
        ]

        # Invoke the model with the prompt.
        response = self.chat_model.invoke(messages)
        return (response.content, {})
