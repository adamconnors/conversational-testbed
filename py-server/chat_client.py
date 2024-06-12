# TODO: Move this into utils when I figure out relative imports !!
import importlib
import shutil
import sys
import textwrap
import click
from main import chat_parameterized
from agents.registry import AgentRegistry
from langchain_core.messages import HumanMessage, AIMessage
from langchain.globals import set_debug
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

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
        /replay - replay the last user_input without updating the history
        /transcript - display a transcript of the conversation so far
        /worldstate - Displays the current world state
        /feedback - Provide feedback on the agent
        /report - Prints a summary report of feedback given so far
        /history - Prints the conversation history so far.
        /exit - End conversation and print a summary report.\n\n""",
        fg="yellow",
    )

    client = ChatClient(agent)
    client.start()


class ChatClient:

    world_state = None
    message_history = []

    def __init__(self, agent):
        self.agent = agent

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
            self.world_state, self.message_history, self.agent, user_input
        )
        response = http_response[0]

        self.world_state = response["world_state"]
        self.message_history.append(HumanMessage(user_input))
        self.message_history.append(AIMessage(response["response"]))

        terminal_width = shutil.get_terminal_size()[0] - SPEAKER_TAG_CHARACTERS
        wrapped_response = textwrap.fill(response["response"], width=terminal_width)
            
        click.echo(
            click.style(f"AI: ", fg="yellow") + click.style(wrapped_response)
        )

    def handle_command(self, command):

        parts = command.split(" ")

        if parts[0] == "replay":
            if len(self.message_history) == 0:
                click.echo(click.style("No messages to repeat", fg="red"))
            else:
                self.message_history.pop()
                last_user_message = self.message_history.pop()
                click.echo(click.style(f"Human (replay): {last_user_message.content}", fg="green"))
                self.process_input(last_user_message.content) 
        elif parts[0] == "transcript":
            click.secho("\n\n---Transcript---\n", fg="yellow")
            for message in self.message_history:
                if isinstance(message, HumanMessage):
                    click.echo(click.style(f"Human: {message.content}", fg="green"))
                else:
                    click.echo(click.style(f"AI: {message.content}", fg="yellow"))
            click.secho("\n\n----------\n", fg="yellow")
        elif parts[0] == "clear":
            self.message_history = []
            self.world_state = None
            click.echo(click.style("Conversation history and world state cleared", fg="yellow"))
        elif parts[0] == "worldstate":
            click.echo(click.style("Not implemented yet", fg="yellow"))
        elif parts[0] == "feedback":
            click.echo(click.style("Not implemented yet", fg="yellow"))
        elif parts[0] == "report":
            click.echo(click.style("Not implemented yet", fg="yellow"))
        elif parts[0] == "history":
            click.echo(click.style("Not implemented yet", fg="yellow"))
        elif parts[0] == "exit":
            click.secho("Conversation ended, report not implemented yet", fg="red")
            exit()
        else:
            click.echo(click.style("Invalid command", fg="red"))

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

    # Set the path to the directory you want to monitor
    #path = "/Users/adamconnors/work/conversational-testbed/py-server"

    # Start the observer
    observer.schedule(event_handler, "./py-server/agents", recursive=True)
    observer.start()
    
    start_chat()
