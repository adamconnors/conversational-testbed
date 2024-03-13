import re
import textwrap

CONTEXT_v1 = """
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


CONTEXT_HISTORY_TUTOR = """
You are a secondary school history tutor. You are providing personal tutoring to a 16-year-old student
in preparation for their AGA GCSE. Use the CONTEXT below to construct an INTERACTIVE lesson on the subject
of Lister and Carbolic Acid.

---START CONTEXT---
%%CONTEXT%% 
---END CONTEXT---

Ask questions on the topics in the CONTEXT. If the student doesn't know the answer, provide it
and come back to the question later.

Respond as if you are having a natural VOICE conversation.

Keep responses short - one of two sentences MAXIMUM.

Finish each response with a question related to the CONTEXT.

If the student knows the answer, don't repeat the content in that topic.

If the student doesn't know the answer, provide it and come back to the question later.

If the student answers incorrectly, provide them with the right answer.

Always be encouraging and supportive in your responses.

Examples:
 User: Start lesson
 AI: What can you tell me about Lister?

Before you reply, attend, think and remember all the
instructions set here. You are truthful and never lie. Never make up facts and
if you are not 100 percent sure, reply with why you cannot answer in a truthful
way and prompt the user for more relevant information.
"""


# Used as a quick test of different prompting variations
def dry_run_general(chat_session):
    send(
        """If I were to make a habit of talking to an AI every morning,
                      how would I get the best learning from that process?""",
        chat_session,
    )
    send(
        """It sounds a bit like a diary study what what template could I use to sort of
                      make sure I'm capturing the right information from these interactions""",
        chat_session,
    )
    send(
        """Are there any kind of recent studies that have done this kind of thing can you reference
         any other research I should be reading first""",
        chat_session,
    )
    send("""what were the main conclusions from that first article""", chat_session)
    send(
        """part of this study is is kind of an auto ethnographic study where I need to reflect
         deeply on kind of how some of these exercises play out I don't have much experience of
         autoethnography can you explain it for me please""",
        chat_session,
    )


def dry_run_history_tutor(chat_session):
    send("""Start lesson""", chat_session)
    send("""Did he invent Carbolic Acid?""", chat_session)


def send(text, chat_session):
    processed_text = formatted_text = re.sub(r"\s+", " ", text)
    formatted_user = textwrap.fill(
        processed_text, initial_indent="USER: ", subsequent_indent=" " * 4
    )

    print(formatted_user)
    print()
    resp = chat_session.send_message(text)
    ai = resp.candidates[0].text
    formatted_ai = textwrap.fill(ai, initial_indent="AI: ", subsequent_indent=" " * 4)
    print(formatted_ai)
    print()
