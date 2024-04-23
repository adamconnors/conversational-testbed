import {Component} from '@angular/core';

@Component({
  selector: 'app-history-tutor',
  templateUrl: './history-tutor.component.html',
  styleUrl: './history-tutor.component.css',
})
export class HistoryTutorComponent {
  worldState: WorldState | undefined;

  getInitialWorldState(): object[] {
    return [];
  }

  // Called when the worldstate is returned from the server.
  updateWorldState(state: object[]): object[] {
    this.worldState = { questions: state as Question[] };

    // TODO: I'm converting into an object model so I can render if more cleanly,
    // but the object model is specific to each module so I end up returning the original
    // JSON object. If the client ends up needing to update the world state this will mean
    // converting it and then converting it back. I need to find a better way to do this.
    return state;
  }

  // TODO: This is because sometimes the model changes the name of the field. I need to
  // use pydantic instead so this is consistent.
  hasAnswered(answer: Answer) {
    if (answer.hasAnswered === true || answer.has_answered === true) {
      return true;
    }
    if (answer.hasAnswered === 'true' || answer.has_answered === 'true') {
      return true;
    }

    return false;
  }

  calculatePercentageComplete() {
    let correctAnswers = 0;
    let totalAnswers = 0;

    if (this.worldState == undefined) {
      return 0;
    }

    for (const question of this.worldState!.questions) {
      for (const answer of question.answers) {
        totalAnswers += 1;
        if (this.hasAnswered(answer)) {
          correctAnswers += 1;
        }
      }
    }
    if (totalAnswers == 0) {
      return 0;
    }
    return Math.round((correctAnswers / totalAnswers) * 100);
  }
}

interface WorldState {
  questions: Question[];
}

interface Question {
  question: string;
  answers: Answer[];
}

// Interface is needed since LLM object is not always consistent.
interface Answer {
  answer: string;
  hasAnswered: boolean | string;
  has_answered: boolean | string;
}
