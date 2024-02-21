import flask
from flask_cors import CORS
from vertexai.language_models import ChatModel, InputOutputTextPair
import base64
import google.cloud.texttospeech_v1 as texttospeech
import prompts

global chat, dry_run_function
chat = None

DRY_RUN_MODE = False
dry_run_function = prompts.dry_run_general

# CHAT_VERSION = "no-prompting"
# CHAT_VERSION = "prompted-v1"
CHAT_VERSION = "prompted-history-tutor"

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = flask.Flask(__name__)
tts_client = texttospeech.TextToSpeechClient()

# TODO: How do I keep the context of this instance of chat for a given user session when running in 
chat_model = ChatModel.from_pretrained("chat-bison@002")


def load_file(filename):
    with open(filename, 'r') as file:
        return file.read()

# Load chat model with prompt.
if CHAT_VERSION == "no-prompting":
    chat = chat_model.start_chat()
elif CHAT_VERSION == "prompted-v1":
    chat = chat_model.start_chat(context=prompts.CONTEXT_v1)
elif CHAT_VERSION == "prompted-history-tutor":
    
    history_tutor_context = prompts.CONTEXT_HISTORY_TUTOR
    lister_and_carbolic_acid_context = load_file("./history_tutor/lister_and_carbolic_acid.md")
    
    history_tutor_context = history_tutor_context.replace("%%CONTEXT%%", lister_and_carbolic_acid_context)
    chat = chat_model.start_chat(context=prompts.CONTEXT_HISTORY_TUTOR)
    dry_run_function = prompts.dry_run_history_tutor


# Combine these to save ourselves a server roundtrip.
@app.route('/tts', methods = ['POST', 'GET'])
def tts():
    text = flask.request.args.get('text') or flask.request.form.get('text')
    text = text.replace('*', '')

    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = tts_client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    audio_bytes = response.audio_content

    # Return audio base64 string
    rtn = audio_bytes, 200, {'Content-Type': 'audio/mpeg', 'Access-Control-Allow-Origin': '*'}
    return rtn
    

@app.route('/api', methods = ['POST', 'GET'])
def api():
    global chat
    
    q = flask.request.args.get('q') or flask.request.form.get('q')
    
    print("Got query: ", q)
    if q is None:
        return "No request sent, use ?q=", 200, cors_headers
    
    # Make request to the server
    resp = chat.send_message(q)
    text = resp.candidates[0].text

    # Text Response
    rtn = text, 200, {'Access-Control-Allow-Origin': '*'}
    return rtn

if __name__ == "__main__":
    
    if not DRY_RUN_MODE:
        # Used when running locally only. When deploying to Google App
        # Engine, a webserver process such as Gunicorn will serve the app. This
        # can be configured by adding an `entrypoint` to app.yaml.
        app.run(host="localhost", port=8080, debug=True)
    else:
        dry_run_function(chat)
            
    