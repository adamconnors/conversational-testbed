import {Component, Input} from '@angular/core';
import {Agent, AgentState} from '@data/agent';

@Component({
  selector: 'app-default-agent',
  templateUrl: './default-agent.component.html',
  styleUrl: './default-agent.component.css',
})
export class DefaultAgentComponent implements Agent {
  @Input() name: string = '';

  processExchange(state: AgentState): AgentState {
    return state;
  }
}
