import {Component, ElementRef, ViewChild} from '@angular/core';
import {SpeechRecognizerComponent} from '@components/speech-recognizer/speech-recognizer.component';
import {ModeSelectorComponent} from '@components/mode-selector/mode-selector.component';
import {ChatService} from '@services/chat.service';
import {ChatMessage, PromptMode} from 'app/data/conversation';
import {debounce} from './util/debounce';
import {HistoryTutorComponent} from '@components/history-tutor/history-tutor.component';
import {FakeModeComponent} from '@components/fake-mode/fake-mode.component';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
})
export class AppComponent {
  @ViewChild(SpeechRecognizerComponent)
  speechRecognizerComponent!: SpeechRecognizerComponent;
  @ViewChild(ModeSelectorComponent)
  modeSelectorComponent!: ModeSelectorComponent;
  @ViewChild('content', {read: ElementRef})
  contentElement!: ElementRef;
  @ViewChild(HistoryTutorComponent)
  historyTutorComponent!: HistoryTutorComponent;
  @ViewChild(FakeModeComponent)
  fakeModeComponent!: FakeModeComponent;

  conversation: ChatMessage[] = [];
  interimDialogLine: string = '';

  // TODO: Create an object definition for this.
  worldState: object[] = [];

  // TODO: Refactor so this is only set in one place.
  currentMode: PromptMode = 'default';

  private debouncedScrollToBottom: () => void;

  constructor(private chatService: ChatService) {
    this.debouncedScrollToBottom = debounce(this.scrollToBottom);
  }

  nAfterViewInit(): void {
    this.currentMode = this.modeSelectorComponent.currentMode;
  }

  handleModeChange(mode: PromptMode) {
    this.currentMode = mode;
  }

  handleNewLineOfDialog(dialog: string) {
    if (!dialog) {
      return;
    }
    const responseObservable = this.chatService.sendMessage(
      dialog,
      this.conversation,
      this.worldState,
      this.modeSelectorComponent.currentMode
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
        this.worldState = this.historyTutorComponent.updateWorldState(
          // TODO: Each module defines its own world state object so we need 
          // a clean way to do this.
          this.worldState as object[]
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
