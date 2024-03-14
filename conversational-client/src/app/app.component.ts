import {Component, ViewChild} from '@angular/core';
import {SpeechRecognizerComponent} from '@components/speech-recognizer/speech-recognizer.component';
import {ModeSelectorComponent} from '@components/mode-selector/mode-selector.component';
import {ChatService} from '@services/chat.service';
import {ChatMessage} from 'app/data/conversation';

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

  conversation: ChatMessage[] = [];
  interimDialogLine: string = '';

  constructor(private chatService: ChatService) {}

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
    });
  }

  handleNewInterimDialogLineEvent(dialog: string) {
    this.interimDialogLine = dialog;
  }

  donwloadTranscript() {
    this.chatService.downloadTranscript(this.conversation);
  }
}
