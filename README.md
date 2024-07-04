# Conversational Toolkit

The Conversational Toolkit is a web application that provides a simple prototyping environment for voice-driven conversational AI agents.

The toolkit fronts a language model with automatic speech recognition (ASR) using the WebSpeech API, and text-to-speech (TTS) using the Vertex speech API. It is designed to be modular so that new use cases can be quickly added with well-encapsulated code changes.

## Local Development

### Start backend server:
To run the server locally, you must first install the Google Cloud CLI and set up your default project and application default credentials.

Follow [Google Cloud Installation Instructions](https://cloud.google.com/sdk/docs/install) to install the Google Cloud CLI.

Follow [Set up Application Default Credentials](https://cloud.google.com/docs/authentication/provide-credentials-adc) to set up application default credentials.

```sh
gcloud auth login

# Ensure your project has the Vertex APIs enabled
gcloud config set project [PROJECT_ID]
gcloud auth application-default login
gcloud auth application-default set-quota-project [PROJECT_ID]
```

```sh
 cd server
 pip install -r requirements.txt
 python3 main.py
```

You can test the server by pointing your browser at:
http://localhost:8080/chat?q=hello

### Start the client development server:
Install npm at: https://nodejs.org/en/download/.

Then:
```sh
cd client
npm install
npm run start
```

Navigate to http://localhost:4200 and click the microphone icon to begin speaking.

## Run tests
**WARNING**: Server scripts make calls to the language-model and will incur charges.

### To run server tests from the **project root**:

```sh
# All tests
python3 -m unittest discover -t . -s server -p "*_test.py"

# A specific test
python3 -m unittest server.agents.fake_agent_test
```

or use the convenience script:
```sh
# All tests
python3 -m server.scripts.run_tests --test_name all

# Named test
python3 -m server.scripts.run_tests --test_name fake_agent_test
```

### To run client tests:
```sh
cd client
npm run ng test
```

## Agent development
Conversational agents are the abstraction used to mediate user/AI interactions.
An agent is implemented as:
- A python class on the server that communicates with an LLM (e.g. prompt-chain + supplementary RAG, integrations, world state).
- An Angular component on the client to drive user interactions through customizable UI.

To create a new agent you will need to add server and client implementations as follows.

#### Server
- Define a new python file or module that subclasses the `ConversationalAgent` base class and implements the `chat` method.
  - See agents.py for the class definition, and default_agent.py for an example implementation.
- Add the new agent with a unique id to `_AGENT_BY_ID` in `agents/registry.py`.

#### Client
- Create an Angular component for your agent:
```sh
npm run ng g component components/agents/your-agent-name
```
- Implement the `Agent` interface (`app/data/agent.ts`) in your component's class (`components/agents/your-agent-name.ts`).

A minimal implementation would just return the `state` object unchanged. Use the `fake_agent` component for reference. For example:

```ts
export class YourAgentComponent implements Agent {
  processExchange(state: AgentState): AgentState {
    return state; 
  }
}
```

- Add a unique identifier for your agent to `AGENT_IDS` in `app/data/agent.ts`.
- Register your agent component and its preferences in `app/services/agents.service.ts`.

After these steps, you should see your agent's name in the app's side bar and selecting it should display its component UI.

## Cloud deployment
Set your cloud project and authenticate as above. To deploy to AppEngine, run:

```sh
cd client
npm run prod

cd ../py-server
gcloud app deploy
```
