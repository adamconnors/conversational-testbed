import {Component} from '@angular/core';
import {Agent, AgentState} from '@data/agent';

interface WorldState {
  question: string;
  answers: Answer[];
}

interface Answer {
  answer: string;
  hasAnswered: boolean;
}

@Component({
  selector: 'app-history-tutor',
  templateUrl: './history-tutor.component.html',
  styleUrl: './history-tutor.component.css',
})
export class HistoryTutorComponent implements Agent {
  worldState: WorldState | null = null;

  // Called when the server responsed.
  processExchange(state: AgentState) {
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
      if (answer.hasAnswered) {
        correctAnswers += 1;
      }
    }
    if (totalAnswers == 0) {
      return 0;
    }
    return Math.round((correctAnswers / totalAnswers) * 100);
  }
}
