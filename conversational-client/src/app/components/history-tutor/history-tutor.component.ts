import {Component} from '@angular/core';

@Component({
  selector: 'app-history-tutor',
  templateUrl: './history-tutor.component.html',
  styleUrl: './history-tutor.component.css',
})
export class HistoryTutorComponent {
  worldStateDisplay: string | undefined = undefined;

  updateWorldState(worldState: object): object {
    this.worldStateDisplay = JSON.stringify(worldState, null, 2);
    return worldState;
  }
}
