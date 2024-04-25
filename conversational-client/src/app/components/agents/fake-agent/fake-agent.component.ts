import {Component} from '@angular/core';
import {NgZone} from '@angular/core';

@Component({
  selector: 'app-fake-agent',
  templateUrl: './fake-agent.component.html',
  styleUrl: './fake-agent.component.css',
})
export class FakeAgentComponent {
  worldStateDisplay: string = '';

  constructor(private zone: NgZone) {}

  updateWorldState(worldState: object): object {
    this.worldStateDisplay = JSON.stringify(worldState);
    return worldState;
  }
}
