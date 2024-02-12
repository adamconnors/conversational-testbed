import { Component, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { SpeechRecognizerComponent } from './speech-recognizer/speech-recognizer.component';
import { APIService } from './api.service';
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

  constructor(private apiService: APIService) {}

  handleNewLineOfDialog(eventData: string) {
    console.log("Got new dialog: " + eventData);
    let responseObservable = this.apiService.getLLMLineOfDialog(eventData);
    
    responseObservable.subscribe( (data: string) => {
      const llmResponse = data;
      this.speechRecognizerComponent.handleLLMResponse(llmResponse);
    });

  }

}
