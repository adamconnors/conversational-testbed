import {Component} from '@angular/core';
import {NgZone} from '@angular/core';

@Component({
  selector: 'app-fake-mode',
  templateUrl: './fake-mode.component.html',
  styleUrl: './fake-mode.component.css',
})
export class FakeModeComponent {
  worldStateDisplay: string = '';
  constructor(private zone: NgZone) {}

  updateWorldState(worldState: object): object {
    this.worldStateDisplay = JSON.stringify(worldState);
    return worldState;
  }
}
