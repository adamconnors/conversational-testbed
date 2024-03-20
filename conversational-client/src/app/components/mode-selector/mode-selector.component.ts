import {Component, EventEmitter, Output} from '@angular/core';
import {PromptMode} from 'app/data/conversation';

@Component({
  selector: 'app-mode-selector',
  templateUrl: './mode-selector.component.html',
  styleUrl: './mode-selector.component.css',
})
export class ModeSelectorComponent {
  modes: PromptMode[] = ['default', 'fake', 'history_tutor'];
  currentMode: PromptMode = 'default';

  @Output() modeChange = new EventEmitter<PromptMode>();

  onSelectMode(mode: PromptMode) {
    this.currentMode = mode;
    this.modeChange.emit(mode);
  }
}
