import {Component} from '@angular/core';
import {AgentState} from '@data/agent';

@Component({
  selector: 'app-help-me-cook',
  standalone: true,
  imports: [],
  templateUrl: './help-me-cook.component.html',
  styleUrl: './help-me-cook.component.css',
})
export class HelpMeCookComponent {
  processExchange(state: AgentState): AgentState {
    return state;
  }
}
