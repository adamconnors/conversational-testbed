import {Component} from '@angular/core';
import {Agent, AgentState} from '@data/agent';

export interface WorldState {
  question: string;
  answers: Answer[];
}

interface Answer {
  answer: string;
  hasAnswered: string;
}

@Component({
  selector: 'app-history-tutor',
  templateUrl: './history-tutor.component.html',
  styleUrl: './history-tutor.component.css',
})
export class HistoryTutorComponent implements Agent {
  worldState: WorldState | null = null;

  // Called when server responds with a new state and chat response.
  processExchange(state: AgentState) {
    console.log(state.worldState);

    this.worldState = state.worldState as WorldState;
    return {...state, worldState: this.worldState};
  }

  calculatePercentageComplete() {
    let correctAnswers = 0;
    let totalAnswers = 0;

    if (this.worldState == undefined) {
      return 0;
    }

    for (const answer of this.worldState.answers) {
      totalAnswers += 1;
      if (answer.hasAnswered === 'true') {
        correctAnswers += 1;
      }
    }
    if (totalAnswers == 0) {
      return 0;
    }
    return Math.round((correctAnswers / totalAnswers) * 100);
  }
}
