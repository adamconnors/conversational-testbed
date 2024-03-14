import {Component} from '@angular/core';
import {PromptMode} from 'app/data/conversation';

@Component({
  selector: 'app-mode-selector',
  templateUrl: './mode-selector.component.html',
  styleUrl: './mode-selector.component.css',
})
export class ModeSelectorComponent {
  modes: PromptMode[] = ['default', 'fake'];
  currentMode: PromptMode = 'default';

  constructor() {}

  onSelectMode(mode: PromptMode) {
    this.currentMode = mode;
  }
}
