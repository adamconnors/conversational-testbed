import json
import flask
from flask_cors import CORS
import google.cloud.texttospeech_v1 as texttospeech
import prompts
from default_agent import DefaultAgent
from fake_agent import FakeAgent
from history_tutor.history_tutor import HistoryTutor
from agents import AgentState
from langchain_core.messages import HumanMessage, AIMessage


DRY_RUN_MODE = False
dry_run_function = prompts.dry_run_general

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = flask.Flask(__name__)
tts_client = texttospeech.TextToSpeechClient()

# Create conversational agents. An agent is a ConversationalAgent subclass.
# It's able to respond to user messages based on the conversation history
# and previous state.
AGENT_BY_ID = {
    "default": DefaultAgent(),
    "fake": FakeAgent(),
    "history_tutor": HistoryTutor(),
}


# Combine these to save ourselves a server roundtrip.
@app.route("/tts", methods=["POST", "GET"])
def tts():
    text = flask.request.args.get("text") or flask.request.form.get("text")
    text = text.replace("*", "")

    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
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
        {"Content-Type": "audio/mpeg", "Access-Control-Allow-Origin": "*"},
    )
    return rtn


@app.route("/chat", methods=["POST", "GET"])
def chat():
    q = flask.request.args.get("q") or flask.request.form.get("q")
    agent_id = flask.request.args.get("agent_id") or flask.request.form.get("agent_id")
    if q is None:
        return "No request sent, use ?q=", 200
    print("q", q)

    # Message History
    message_history_json = flask.request.args.get(
        "message_history"
    ) or flask.request.form.get("message_history")
    message_history = build_message_history(message_history_json)

    # World State
    world_state_json = flask.request.args.get("world_state") or flask.request.form.get(
        "world_state"
    )
    world_state = json.loads(world_state_json) if world_state_json else None
    print(f"World state in main: {world_state}")

    # Get the right model for this use-case
    if agent_id in AGENT_BY_ID:
        agent = AGENT_BY_ID[agent_id]
    else:
        agent = AGENT_BY_ID["default"]

    print(f"Responding with {agent}.")
    agent_response, agent_world_state = agent.chat(AgentState(q, message_history, world_state))

    # TODO: Can we skip this step and pass it directly to the response?
    response = {
        "response": agent_response,
        "world_state": agent_world_state,
    }

    return response, 200, {"Access-Control-Allow-Origin": "*"}


def build_message_history(message_history_json):
    """Parses client provided message history into ChatMessage objects

    Args:
        message_history_json (_type_): [ {content="xxx", author="AI|USER"} ]

    Returns:
        list[langchain.BaseMessage]: List of either AIMessage or HumanMessage
        objects, or None if empty list.

    Raises:
        ValueError: If the message author is neither "ai" nor "human" or the
        message history can't be parsed.
    """
    messages = []
    if not message_history_json:
        return messages
    try:
        for message in json.loads(message_history_json):
            if message["author"] == "human":
                messages.append(HumanMessage(message["content"]))
            elif message["author"] == "ai":
                messages.append(AIMessage(message["content"]))
            else:
                raise ValueError(f"Unknown message type: {message}")
    except Exception as e:
        raise ValueError(f"Couldn't parse message history: {message_history_json}: {e}")
    return messages


if __name__ == "__main__":
    if not DRY_RUN_MODE:
        # Used when running locally only. When deploying to Google App
        # Engine, a webserver process such as Gunicorn will serve the app. This
        # can be configured by adding an `entrypoint` to app.yaml.
        app.run(host="localhost", port=8080, debug=True)
    else:
        pass
        # Temporarily disable
        # dry_run_function(chat_model.start_chat(context=chat_context))
