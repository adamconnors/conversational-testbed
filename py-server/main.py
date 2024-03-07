import json
import flask
from flask_cors import CORS
import google.cloud.texttospeech_v1 as texttospeech
import prompts
from vertexai.language_models import ChatMessage, ChatModel


CHAT_VERSION = 'prompted-v1' # 'no-prompting'|'prompted-history-tutor'
DRY_RUN_MODE = False
dry_run_function = prompts.dry_run_general

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = flask.Flask(__name__)
tts_client = texttospeech.TextToSpeechClient()

chat_model = ChatModel.from_pretrained('chat-bison@002')
chat_context = ''


def load_file(filename):
  with open(filename, 'r') as file:
    return file.read()


# Load chat context.
if CHAT_VERSION == 'prompted-v1':
  chat_context = prompts.CONTEXT_v1
elif CHAT_VERSION == 'prompted-history-tutor':
  history_tutor_context = prompts.CONTEXT_HISTORY_TUTOR
  lister_and_carbolic_acid_context = load_file(
      './history_tutor/lister_and_carbolic_acid.md'
  )
  history_tutor_context = history_tutor_context.replace(
      '%%CONTEXT%%', lister_and_carbolic_acid_context
  )
  dry_run_function = prompts.dry_run_history_tutor


# Combine these to save ourselves a server roundtrip.
@app.route('/tts', methods=['POST', 'GET'])
def tts():
  text = flask.request.args.get('text') or flask.request.form.get('text')
  text = text.replace('*', '')

  synthesis_input = texttospeech.SynthesisInput(text=text)
  voice = texttospeech.VoiceSelectionParams(
      language_code='en-US', ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
  )
  audio_config = texttospeech.AudioConfig(
      audio_encoding=texttospeech.AudioEncoding.MP3
  )
  response = tts_client.synthesize_speech(
      input=synthesis_input, voice=voice, audio_config=audio_config
  )
  audio_bytes = response.audio_content

  # Return audio base64 string
  rtn = (
      audio_bytes,
      200,
      {'Content-Type': 'audio/mpeg', 'Access-Control-Allow-Origin': '*'},
  )
  return rtn


@app.route('/chat', methods=['POST', 'GET'])
def chat():
  q = flask.request.args.get('q') or flask.request.form.get('q')
  if q is None:
    return 'No request sent, use ?q=', 200
  print('q', q)

  message_history_json = flask.request.args.get(
      'message_history'
  ) or flask.request.form.get('message_history')
  message_history = None
  try:
    # Assume user takes first turn.
    message_history = [
        ChatMessage(content=msg, author='user')
        if i % 2 == 0 else ChatMessage(content=msg, author='bot')
        for i, msg in enumerate(json.loads(message_history_json))
    ]
    print('message_history', message_history)
    if not message_history:
      # Don't send an empty message history list
      message_history = None
  except Exception as e:
    print('failed to parse chat history', e)

  chat_session = chat_model.start_chat(
      context=chat_context, message_history=message_history
  )
  res = chat_session.send_message(q)
  text = res.candidates[0].text
  return text, 200, {'Access-Control-Allow-Origin': '*'}


if __name__ == '__main__':
  if not DRY_RUN_MODE:
    # Used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='localhost', port=8080, debug=True)
  else:
    dry_run_function(chat_model.start_chat(context=chat_context))

