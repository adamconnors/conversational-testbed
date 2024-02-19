import textwrap
import re
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

global chat

# Used as a quick test of different prompting variations
def dry_run(chat_instance):
    global chat
    chat = chat_instance
    send("""If I were to make a habit of talking to an AI every morning,
                      how would I get the best learning from that process?""")
    send("""It sounds a bit like a diary study what what template could I use to sort of
                      make sure I'm capturing the right information from these interactions""")
    send("""Are there any kind of recent studies that have done this kind of thing can you reference
         any other research I should be reading first""")
    send("""what were the main conclusions from that first article""")
    send("""part of this study is is kind of an auto ethnographic study where I need to reflect
         deeply on kind of how some of these exercises play out I don't have much experience of
         autoethnography can you explain it for me please""")
    
def send(text):
    
    processed_text = formatted_text = re.sub(r'\s+', ' ', text)
    formatted_user = textwrap.fill(processed_text, initial_indent="USER: ", subsequent_indent=" " * 4)
    
    print(formatted_user)
    print()
    resp = chat.send_message(text)
    ai = resp.candidates[0].text
    formatted_ai = textwrap.fill(ai, initial_indent="AI: ", subsequent_indent=" " * 4)
    print(formatted_ai)
    print()
