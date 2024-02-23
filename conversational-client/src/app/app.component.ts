import { Component, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { SpeechRecognizerComponent } from './speech-recognizer/speech-recognizer.component';
import { ChatService } from './chat.service';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet, SpeechRecognizerComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {

  @ViewChild(SpeechRecognizerComponent) speechRecognizerComponent!: SpeechRecognizerComponent;

  title = 'conversational-client';

  constructor(private chatService: ChatService) {}

  handleNewLineOfDialog(dialog: string[]) {
    const newLine = dialog.at(-1);
    if (!newLine) {
      return;
    }
    console.log("Got new dialog: ", newLine);
    const message_history = dialog.slice(0, -1);
    const responseObservable = this.chatService.getLLMLineOfDialog(newLine, message_history);
    
    responseObservable.subscribe((llmResponse: string) => {
      this.speechRecognizerComponent.handleLLMResponse(llmResponse);
    });

  }

}
