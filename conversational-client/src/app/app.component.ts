import {
  AfterViewChecked,
  Component,
  ElementRef,
  OnInit,
  ViewChild,
} from '@angular/core';
import {SpeechRecognizerComponent} from '@components/speech-recognizer/speech-recognizer.component';
import {AgentSelectorComponent} from '@components/agent-selector/agent-selector.component';
import {ChatService} from '@services/chat.service';
import {ChatMessage, AgentId, AGENT_IDS} from 'app/data/conversation';
import {debounce} from './util/debounce';
import {HistoryTutorComponent} from '@components/agents/history-tutor/history-tutor.component';
import {FakeAgentComponent} from '@components/agents/fake-agent/fake-agent.component';
import {ActivatedRoute} from '@angular/router';
import {Agent, AgentState} from '@data/conversation';

// Conversational agent without UI or world state.
class DefaultAgent implements Agent {
  updateState(state: AgentState) {
    return state;
  }
}

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
})
export class AppComponent implements OnInit, AfterViewChecked {
  @ViewChild(SpeechRecognizerComponent)
  speechRecognizerComponent!: SpeechRecognizerComponent;
  @ViewChild(AgentSelectorComponent)
  agentSelectorComponent!: AgentSelectorComponent;
  @ViewChild('content', {read: ElementRef})
  contentElement!: ElementRef;
  @ViewChild(HistoryTutorComponent)
  historyTutorComponent!: HistoryTutorComponent;
  @ViewChild(FakeAgentComponent)
  fakeAgentComponent!: FakeAgentComponent;

  conversation: ChatMessage[] = [];
  interimDialogLine: string = '';

  agentId: AgentId = 'default';
  private agentRegistry: {[k in AgentId]: Agent} | null = null;
  private agentState: AgentState = {messageHistory: [], worldState: {}};

  private debouncedScrollToBottom: () => void;

  constructor(
    private chatService: ChatService,
    private route: ActivatedRoute
  ) {
    this.debouncedScrollToBottom = debounce(this.scrollToBottom);
  }

  ngOnInit() {
    this.route.queryParamMap.subscribe(params => {
      const agentIdParam = params.get('agent');
      if (AGENT_IDS.includes(agentIdParam as AgentId)) {
        this.agentId = agentIdParam as AgentId;
      }
    });
  }

  ngAfterViewChecked() {
    // Initialize the agent registries once child views are ready.
    this.agentRegistry = {
      default: new DefaultAgent(),
      fake: this.fakeAgentComponent,
      history_tutor: this.historyTutorComponent,
    };
  }

  handleNewLineOfDialog(dialog: string) {
    if (!dialog) {
      return;
    }
    const responseObservable = this.chatService.sendMessage(
      dialog,
      this.conversation,
      this.agentState.worldState as object,
      this.agentId
    );
    responseObservable.subscribe((llmResponse: string) => {
      // Update the UI only once, when we receive the LLM response.
      this.interimDialogLine = '';

      const parsedResponse = JSON.parse(llmResponse);
      const llmDialog = parsedResponse['response'];
      const worldState = parsedResponse['world_state'];
      const userMessage = {content: dialog, author: 'user'};
      const llmMessage = {content: llmDialog, author: 'llm'};
      this.conversation = [...this.conversation, userMessage, llmMessage];
      this.speechRecognizerComponent.handleLLMResponse(llmDialog);

      const agentState = {messageHistory: this.conversation, worldState};
      const agent = this.agentRegistry![this.agentId];
      if (agent) {
        this.agentState = agent.updateState(agentState);
      }

      this.debouncedScrollToBottom();
    });
  }

  handleNewInterimDialogLineEvent(dialog: string) {
    this.interimDialogLine = dialog;
  }

  donwloadTranscript() {
    this.chatService.downloadTranscript(this.conversation);
  }

  private scrollToBottom() {
    this.contentElement.nativeElement.scroll({
      top: this.contentElement.nativeElement.scrollHeight,
      left: 0,
      behavior: 'smooth',
    });
  }
}
