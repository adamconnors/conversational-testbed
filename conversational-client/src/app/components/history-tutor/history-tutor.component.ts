import {Component} from '@angular/core';

@Component({
  selector: 'app-history-tutor',
  templateUrl: './history-tutor.component.html',
  styleUrl: './history-tutor.component.css',
})
export class HistoryTutorComponent {
  worldState: WorldState | undefined = undefined;

  getInitialWorldState(): object[] {
    return [];
  }

  // Called when the worldstate is returned from the server.
  updateWorldState(state: object[]): object[] {
    console.log("Got updated world state");
    console.log(state);
    const questions: Question[] = [];
    for (const question of state) {
      questions.push(question as Question);
    }
    this.worldState = {questions: questions};

    // TODO: I'm converting into an object model so I can render if more cleanly,
    // but the object model is specific to each module so I end up returning the original
    // JSON object. If the client ends up needing to update the world state this will mean
    // converting it and then converting it back. I need to find a better way to do this.
    return state;
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
        if (answer.hasAnswered == true) {
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

interface Answer {
  answer: string;
  hasAnswered: boolean;
}
