import {Component, EventEmitter, inject, Input, Output} from '@angular/core';
import {AgentId} from '@data/agent';
import {AgentsService} from '@services/agents.service';

@Component({
  selector: 'app-agent-selector',
  templateUrl: './agent-selector.component.html',
  styleUrl: './agent-selector.component.css',
})
export class AgentSelectorComponent {
  private readonly agentConfigs = inject(AgentsService).getAgentConfigs();

  @Input() selectedAgentId: AgentId | null = null;

  @Output() selectedAgentIdChange = new EventEmitter<AgentId>();

  get _agentIds() {
    return [...this.agentConfigs.keys()];
  }

  agentSelectionChanged(agentId: AgentId) {
    this.selectedAgentId = agentId;
    this.selectedAgentIdChange.emit(agentId);
  }

  getAgentDisplayName(agentId: AgentId) {
    const config = this.agentConfigs.get(agentId)!;
    return config.preferences.displayName;
  }
}
