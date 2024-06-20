import json
import flask
import google.cloud.texttospeech_v1 as texttospeech

from .agents.agents import AgentState
from .agents.registry import AgentRegistry
from langchain_core.messages import HumanMessage, AIMessage


# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = flask.Flask(__name__)
tts_client = texttospeech.TextToSpeechClient()
agent_registry = AgentRegistry()


# Combine these to save ourselves a server roundtrip.
@app.route("/tts", methods=["POST", "GET"])
def tts():
    text = flask.request.args.get("text") or flask.request.form.get("text")
    text = text.replace("*", "").replace("#", "")

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
    return (
        audio_bytes,
        200,
        {"Content-Type": "audio/mpeg", "Access-Control-Allow-Origin": "*"},
    )


@app.route("/_ah/warmup")
def warmup():
    print("Warm up called.")
    return "", 200, {}


@app.route("/chat", methods=["POST", "GET"])
def chat():
    """Handles incoming chat requests, processes them using the specified agent,
    and returns the agent's response along with the updated world state.
    """
    q = flask.request.args.get("q") or flask.request.form.get("q")
    agent_id = flask.request.args.get("agent_id") or flask.request.form.get("agent_id")
    if q is None:
        return "No request sent, use ?q=", 200
    print("q", q)

    # Message History
    message_history_json = flask.request.args.get(
        "message_history"
    ) or flask.request.form.get("message_history")

    # World State
    world_state_json = flask.request.args.get("world_state") or flask.request.form.get(
        "world_state"
    )
    world_state = json.loads(world_state_json) if world_state_json else None
    message_history = build_message_history(message_history_json)

    # Get the right model for this use-case
    if not agent_registry.is_agent_registered(agent_id):
        print(f"WARNING: Agent ID {agent_id} not found in registry. Using default.")
        agent_id = "default"
    agent = agent_registry.get_agent(agent_id)

    agent_response, agent_world_state = agent.chat(
        AgentState(q, message_history, world_state)
    )

    return (
        {
            "response": agent_response,
            "world_state": agent_world_state,
        },
        200,
        {"Access-Control-Allow-Origin": "*"},
    )


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
    app.run(host="localhost", port=8080, debug=True)
