import {Component} from '@angular/core';

@Component({
  selector: 'app-history-tutor',
  templateUrl: './history-tutor.component.html',
  styleUrl: './history-tutor.component.css',
})
export class HistoryTutorComponent {
  worldState: object | undefined = undefined;
  worldStateDisplay: string | undefined = undefined;

  updateWorldState(worldState: object): object {
    this.worldState = worldState;
    this.worldStateDisplay = JSON.stringify(worldState);
    return worldState;
  }
}
