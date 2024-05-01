import {Component, Injectable} from '@angular/core';
import {Agent, AgentId} from '@data/agent';

import {HistoryTutorComponent} from '@components/agents/history-tutor/history-tutor.component';
import {FakeAgentComponent} from '@components/agents/fake-agent/fake-agent.component';
import {DefaultAgentComponent} from '@components/agents/default-agent/default-agent.component';

export interface AgentComponentConstructor {
  new (): Agent & Component;
}

export interface AgentComponentPreferences {
  displayName: string;
  shouldDisplayChat: boolean;
  shouldTruncateChatHistory: boolean;
}

export interface AgentComponentConfig {
  component: AgentComponentConstructor;
  inputs: Record<string, unknown>;
  preferences: AgentComponentPreferences;
}

@Injectable({
  providedIn: 'root',
})
export class AgentsService {
  // Returns an agent component repository keyed by agent id.
  // New agents should be registered here.
  getAgentConfigs(): Map<AgentId, AgentComponentConfig> {
    return new Map<AgentId, AgentComponentConfig>([
      [
        'default',
        {
          component: DefaultAgentComponent,
          inputs: {
            name: 'Gemini',
          },
          preferences: {
            displayName: 'Default Agent',
            shouldDisplayChat: true,
            shouldTruncateChatHistory: false,
          },
        },
      ],
      [
        'fake',
        {
          component: FakeAgentComponent,
          inputs: {},
          preferences: {
            displayName: 'Fake Agent',
            shouldDisplayChat: true,
            shouldTruncateChatHistory: false,
          },
        },
      ],
      [
        'history_tutor',
        {
          component: HistoryTutorComponent,
          inputs: {},
          preferences: {
            displayName: 'History Tutor',
            shouldDisplayChat: true,
            shouldTruncateChatHistory: true,
          },
        },
      ],
    ]);
  }
}
