# TODO: Move this into utils when I figure out relative imports !!
import importlib
import shutil
import sys
import textwrap
import click

# TODO: Move chat_parameterized out of main and instantiate agent_registry.
from main import chat_parameterized, agent_registry
from langchain_core.messages import HumanMessage, AIMessage
from langchain.globals import set_debug
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from model_alignment import single_run
from model_aligner_helper import VertexModelHelper

# Compensates for the speaker tag when setting the
# with of the text to match the width of the terminal.
SPEAKER_TAG_CHARACTERS = 6


@click.command()
@click.option(
    "--agent",
    default="default",
    help="The name of the agent you want to interact with to.",
)
def start_chat(agent):

    click.echo(
        click.style("Test conversation started with ", fg="yellow")
        + click.style(agent, fg="red")
    )
    click.secho(
        f"""Use / to issue commands:
        /clear - clear the conversation and world state
        /undo - undo the last user_input and response
        /transcript - display a transcript of the conversation so far
        /worldstate - Displays the current world state
        /feedback - Provide feedback on the agent or list feedback given so far
        /principles - Generates principles based on feedback to add to the prompt
        /exit - End conversation and print a summary report.\n\n""",
        fg="yellow",
    )

    client = ChatClient(agent)
    client.start()


class ChatClient:

    world_state = None
    message_history = []
    feedback = []

    def __init__(self, agent_name):
        self.agent_name = agent_name

    def start(self):
        while True:
            user_input = click.prompt(click.style("You", fg="green"), type=str)

            if user_input.startswith("/"):
                command = user_input[1:]
                self.handle_command(command)
            else:
                self.process_input(user_input)

    def process_input(self, user_input):
        http_response = chat_parameterized(
            self.world_state, self.message_history, self.agent_name, user_input
        )
        response = http_response[0]

        self.world_state = response["world_state"]
        self.message_history.append(HumanMessage(user_input))
        self.message_history.append(AIMessage(response["response"]))

        terminal_width = shutil.get_terminal_size()[0] - SPEAKER_TAG_CHARACTERS
        wrapped_response = textwrap.fill(response["response"], width=terminal_width)

        click.echo(click.style(f"AI: ", fg="yellow") + click.style(wrapped_response))

    def handle_command(self, command):
        parts = command.split(" ")
        command = parts[0]
        data = " ".join(parts[1:]) if len(parts) > 1 else None

        if command == "undo":
            if len(self.message_history) == 0:
                click.echo(click.style("No messages to undo", fg="red"))
            else:
                last_ai_message = self.message_history.pop()
                last_user_message = self.message_history.pop()
                click.echo(
                    click.style(
                        f"Removed conversation: \n\tHuman: {last_user_message.content} \n\tAI: {last_ai_message.content}",
                        fg="green",
                    )
                )
        elif command == "transcript":
            click.secho("\n\n---Transcript---\n", fg="yellow")
            for message in self.message_history:
                if isinstance(message, HumanMessage):
                    click.echo(click.style(f"Human: {message.content}", fg="green"))
                else:
                    click.echo(click.style(f"AI: {message.content}", fg="yellow"))
            click.secho("\n\n----------\n", fg="yellow")
        elif command == "clear":
            self.message_history = []
            self.world_state = None
            click.echo(
                click.style("Conversation history and world state cleared", fg="yellow")
            )
        elif command == "worldstate":
            click.echo(click.style("Not implemented yet", fg="yellow"))
        elif parts[0] == "feedback":
            if data is None:
                click.secho("\n\n---Transcript---\n", fg="yellow")
                for fb in self.feedback:
                    click.echo(click.style(f"{fb}", fg="green"))
                click.secho("\n----------\n", fg="yellow")
            else:
                click.secho(f"Feedback recorded: {data}", fg="green")
                self.feedback.append(data)
        elif command == "principles":
            self.generate_principles()
        elif parts[0] == "exit":
            click.secho("Conversation ended, report not implemented yet", fg="red")
            exit()
        else:
            click.echo(click.style("Invalid command", fg="red"))

    def generate_principles(self):
        """
        Generate principles based on the feedback given so far. See:
        https://github.com/PAIR-code/model-alignment/tree/e9ced83f910bca926ca42830567a70fe3cb67821
        for more details. Generated principles can be added to be prompt to guide the model.
        """
        if len(self.feedback) == 0:
            click.secho("No feedback given so far", fg="red")
            return

        agent = agent_registry.get_agent(self.agent_name)
        prompt = single_run.ConstitutionalPrompt()
        prompt.conversations = self.generate_conversation_turns(self.message_history)

        single_run_prompt = single_run.AlignableSingleRun(
            VertexModelHelper(), data=prompt
        )
        single_run_prompt.set_model_description(agent.get_system_prompt())
        single_run_prompt.current_convo_idx = len(prompt.conversations) - 1

        for feedback in self.feedback:
            print(f"Creating principles for feedback: {feedback}")
            self.principles = single_run_prompt.critique_response(feedback)

        click.secho("--- Principles generated: ---\n", fg="green")
        for principle in self.principles:
            click.secho("\t" + principle, fg="yellow")
        click.secho("------\n", fg="green")
        click.secho(
            "Add these principles to your prompt to update model behaviour.\n",
            fg="green",
        )

    def generate_conversation_turns(self, message_history):
        """
        Generate conversation turns based on the message history. This is used to
        generate principles based on the feedback given so far.
        """
        turns = []

        turns = []
        for i in range(0, len(message_history), 2):
            pair = message_history[i : i + 2]
            turn_user = single_run.ConversationTurn()
            turn_ai = single_run.ConversationTurn()
            turn_user.is_user = True
            turn_user.text = pair[0].content
            turn_ai.is_user = False
            turn_ai.text = pair[1].content
            turns.append([turn_user, turn_ai])
        return turns


# Define the event handler class
class FileUpdateHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory and not "__pycache__" in event.src_path:

            # Reload all imported modules in the current directory and subdirectories.
            for module_name, module in sys.modules.copy().items():
                if (
                    hasattr(module, "__file__")
                    and module.__file__
                    and os.path.abspath(module.__file__).startswith(os.getcwd())
                    and module_name.startswith("agents.")
                ):
                    importlib.reload(module)  # Reload the module

            click.secho("File change detected, reloaded agent.", fg="yellow")


if __name__ == "__main__":

    # Create an observer and attach the event handler
    observer = Observer()
    event_handler = FileUpdateHandler()

    # Start the observer
    
    observer_directory = os.getcwd() + "/agents"
    observer.schedule(event_handler, observer_directory, recursive=True)
    observer.start()

    start_chat()
