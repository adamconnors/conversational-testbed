import {Component, ElementRef, OnInit, ViewChild} from '@angular/core';
import {SpeechRecognizerComponent} from '@components/speech-recognizer/speech-recognizer.component';
import {AgentSelectorComponent} from '@components/agent-selector/agent-selector.component';
import {ChatService} from '@services/chat.service';
import {ChatMessage, AgentId, AGENT_IDS} from 'app/data/conversation';
import {debounce} from './util/debounce';
import {HistoryTutorComponent} from '@components/history-tutor/history-tutor.component';
import {FakeModeComponent} from '@components/fake-mode/fake-mode.component';
import {ActivatedRoute} from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
})
export class AppComponent implements OnInit {
  @ViewChild(SpeechRecognizerComponent)
  speechRecognizerComponent!: SpeechRecognizerComponent;
  @ViewChild(AgentSelectorComponent)
  agentSelectorComponent!: AgentSelectorComponent;
  @ViewChild('content', {read: ElementRef})
  contentElement!: ElementRef;
  @ViewChild(HistoryTutorComponent)
  historyTutorComponent!: HistoryTutorComponent;
  @ViewChild(FakeModeComponent)
  fakeModeComponent!: FakeModeComponent;

  conversation: ChatMessage[] = [];
  interimDialogLine: string = '';

  // TODO: Create an object definition for this.
  worldState: object = {};

  agentId: AgentId | null = 'default';

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

  handleNewLineOfDialog(dialog: string) {
    if (!dialog || !this.agentId) {
      return;
    }
    const responseObservable = this.chatService.sendMessage(
      dialog,
      this.conversation,
      this.worldState,
      this.agentId
    );
    responseObservable.subscribe((llmResponse: string) => {
      // Update the UI only once, when we receive the LLM response.
      this.interimDialogLine = '';

      const parsedResponse = JSON.parse(llmResponse);
      const llmDialog = parsedResponse['response'];
      this.worldState = parsedResponse['world_state'];
      const userMessage = {content: dialog, author: 'user'};
      const llmMessage = {content: llmDialog, author: 'llm'};
      this.conversation = [...this.conversation, userMessage, llmMessage];
      this.speechRecognizerComponent.handleLLMResponse(llmDialog);

      // TODO: Make this an interface so it's easy to add
      // new components that can handle world state.
      if (this.historyTutorComponent) {
        // TODO: This is temporarily broken while fixing up APIs.
        this.worldState = this.historyTutorComponent.updateWorldState(
          []
        );
      }

      if (this.fakeModeComponent) {
        this.worldState = this.fakeModeComponent.updateWorldState(
          this.worldState
        );
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
