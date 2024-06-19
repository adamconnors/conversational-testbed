import {Component} from '@angular/core';
import {Agent, AgentState} from '@data/agent';

@Component({
  selector: 'app-physics-expert',
  standalone: true,
  imports: [],
  templateUrl: './physics-expert.component.html',
  styleUrl: './physics-expert.component.css',
})
export class PhysicsExpertComponent implements Agent {
  processExchange(state: AgentState): AgentState {
    return state;
  }
}
