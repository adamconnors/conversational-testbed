import {Component} from '@angular/core';
import {Agent, AgentState} from '@data/conversation';

interface FakeAgentWorldState {
  last_message: string;
  message_count: number;
}

function isValidWorldState(state: unknown): state is FakeAgentWorldState {
  return (
    state !== null &&
    typeof state === 'object' &&
    'last_message' in state &&
    'message_count' in state
  );
}

@Component({
  selector: 'app-fake-agent',
  templateUrl: './fake-agent.component.html',
  styleUrl: './fake-agent.component.css',
})
export class FakeAgentComponent implements Agent {
  private worldState: FakeAgentWorldState = {
    last_message: '',
    message_count: 0,
  };
  worldStateDisplay: string = '';

  updateState(state: AgentState) {
    if (!isValidWorldState(state.worldState)) {
      throw new Error('invalid world state');
    }
    this.worldState = state.worldState;
    this.worldState.message_count = state.messageHistory.length;
    this.worldStateDisplay = JSON.stringify(this.worldState);
    return {...state, worldState: this.worldState};
  }
}
