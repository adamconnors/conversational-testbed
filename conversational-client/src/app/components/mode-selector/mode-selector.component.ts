import {Component} from '@angular/core';
import {ChatService} from '@services/chat.service';

@Component({
  selector: 'app-mode-selector',
  templateUrl: './mode-selector.component.html',
  styleUrl: './mode-selector.component.css',
})
export class ModeSelectorComponent {
  // The server expects a mode param that matches the lowercase version of one of these string
  modes = ['Default', 'Fake', 'Gemini', 'History Tutor'];
  currentMode = 'Default';

  constructor(private chatService: ChatService) {}

  onSelectMode(mode: string) {
    this.currentMode = mode;
    this.chatService.setMode(mode.toLowerCase());
  }
}
