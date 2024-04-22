import {Component, EventEmitter, Input, Output} from '@angular/core';
import {AGENT_IDS, AgentId} from 'app/data/conversation';

@Component({
  selector: 'app-agent-selector',
  templateUrl: './agent-selector.component.html',
  styleUrl: './agent-selector.component.css',
})
export class AgentSelectorComponent {
  readonly _agentIds = AGENT_IDS;

  @Input() selectedAgentId: AgentId | null = null;

  @Output() selectedAgentIdChange = new EventEmitter<AgentId>();

  agentSelectionChanged(agentId: AgentId) {
    this.selectedAgentId = agentId;
    this.selectedAgentIdChange.emit(agentId);
  }

  getAgentDisplayName(agentId: AgentId) {
    switch (agentId) {
      case 'default':
        return 'Default Agent';
      case 'fake':
        return 'Fake Agent';
      case 'history_tutor':
        return 'History Tutor';
      default:
        return agentId;
    }
  }
}
