import {Component} from '@angular/core';
import {ChatService} from '@services/chat.service';

type PromptMode = 'default' | 'fake';

@Component({
  selector: 'app-mode-selector',
  templateUrl: './mode-selector.component.html',
  styleUrl: './mode-selector.component.css',
})
export class ModeSelectorComponent {
  // Passed to the server to control the model used for the chat.
  modes: PromptMode[] = ['default', 'fake'];
  currentMode: PromptMode = 'default';

  constructor(private chatService: ChatService) {}

  onSelectMode(mode: PromptMode) {
    this.currentMode = mode;
    this.chatService.setMode(mode);
  }
}
