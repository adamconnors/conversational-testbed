//https://developer.chrome.com/blog/voice-driven-web-apps-introduction-to-the-web-speech-api

import { NgFor } from '@angular/common';
import { Component } from '@angular/core';
import { NgZone, Output, EventEmitter } from '@angular/core';
declare var webkitSpeechRecognition: any;

@Component({
  selector: 'app-speech-recognizer',
  standalone: true,
  imports: [NgFor],
  templateUrl: './speech-recognizer.component.html',
  styleUrl: './speech-recognizer.component.css'
})
export class SpeechRecognizerComponent {

  final_transcript = "";
  recognizing = false;
  ignore_onend = false;
  start_timestamp = 0;
  recognition: any;
  currentLine = 0;

  dialog: string[] = [];

  @Output() newDialogLineEvent = new EventEmitter<string>();

  constructor(private zone: NgZone) { 
    if ( !('webkitSpeechRecognition' in window) ) {
      console.log("webkitSpeechRecognition not found in window");
      return;
    }

    this.recognition = new webkitSpeechRecognition();
    this.recognition.continuous = true;
    this.recognition.interimResults = true;
  
    this.recognition.onstart = () => {
      this.recognizing = true;
      console.log('info_speak_now');
    };
  
    this.recognition.onerror = (event: any) => {
      if (event.error == 'no-speech') {
        console.log('info_no_speech');
        this.ignore_onend = true;
      }
      if (event.error == 'audio-capture') {
        console.log('info_no_microphone');
        this.ignore_onend = true;
      }
      if (event.error == 'not-allowed') {
        if (event.timeStamp - this.start_timestamp < 100) {
          console.log('info_blocked');
        } else {
          console.log('info_denied');
        }
        this.ignore_onend = true;
      }
    };
  
    // called by speech recognition engine
    this.recognition.onend = () => {
      console.log('info_end');
      this.zone.run(() => {
        this.recognizing = false;
      });
    };
  
    // called by speech recognition engine
    this.recognition.onresult = (event: any) => {
      console.log("onresult:" + event.results);
      this.zone.run(() => {
        this.updateDialog(event);
      });
    };
  }

  updateDialog(event: any) {
    let interim_transcript = '';
    for (let i = event.resultIndex; i < event.results.length; ++i) {
      if (event.results[i].isFinal) {
        let line: string = event.results[i][0].transcript;
        this.dialog[this.currentLine] = line;
        this.currentLine++;

        // Emit an event in app.component
        this.newDialogLineEvent.emit(line);
        
      } else {
        interim_transcript += event.results[i][0].transcript;
      }
    }
    if (interim_transcript !== '') {
      this.dialog[this.currentLine] = interim_transcript;
    }

    // Scroll to the bottom of the page
    window.scrollTo(0, document.body.scrollHeight);
  }
  
  handleLLMResponse(response: string) {
    this.dialog[this.currentLine] = response;
    this.currentLine++;
  }

  // Called by user button press. 
  onStartStop() {
    if (this.recognizing) {
      console.log("stop listening");
      this.recognition.stop();
      this.recognizing = false;
    } else {
      console.log("start listening");
      this.recognition.lang = "en-GB";
      this.recognition.start();
      this.recognizing = true;
      this.ignore_onend = true;
      this.start_timestamp = Date.now(); // Assign current timestamp  
    }
  }
}