import {Component, ElementRef, ViewChild} from '@angular/core';
import {SpeechRecognizerComponent} from '@components/speech-recognizer/speech-recognizer.component';
import {ModeSelectorComponent} from '@components/mode-selector/mode-selector.component';
import {ChatService} from '@services/chat.service';
import {ChatMessage} from 'app/data/conversation';
import {debounce} from './util/debounce';

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
  @ViewChild('content', {read: ElementRef}) contentElement!: ElementRef;

  conversation: ChatMessage[] = [];
  interimDialogLine: string = '';

  private debouncedScrollToBottom: () => void;

  constructor(private chatService: ChatService) {
    this.debouncedScrollToBottom = debounce(this.scrollToBottom);
  }

  handleNewLineOfDialog(dialog: string) {
    if (!dialog) {
      return;
    }
    console.log('Got new dialog: ', dialog);
    const responseObservable = this.chatService.getLLMLineOfDialog(
      dialog,
      this.conversation,
      this.modeSelectorComponent.currentMode
    );
    responseObservable.subscribe((llmResponse: string) => {
      // Update the UI only once, when we receive the LLM response.
      this.interimDialogLine = '';
      const userMessage = {content: dialog, author: 'user'};
      const llmMessage = {content: llmResponse, author: 'llm'};
      this.conversation = [...this.conversation, userMessage, llmMessage];
      this.speechRecognizerComponent.handleLLMResponse(llmResponse);
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
