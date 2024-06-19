import {Component, Injectable} from '@angular/core';
import {Agent, AgentId} from '@data/agent';

import {HistoryTutorComponent} from '@components/agents/history-tutor/history-tutor.component';
import {FakeAgentComponent} from '@components/agents/fake-agent/fake-agent.component';
import {DefaultAgentComponent} from '@components/agents/default-agent/default-agent.component';
import {PhysicsExpertComponent} from '@components/agents/physics-expert/physics-expert.component';

export interface AgentComponentConstructor {
  new (): Agent & Component;
}

export interface AgentComponentPreferences {
  // Required preferences for all agents.
  readonly displayName: string;
  // Optional preferences default to false
  readonly shouldHideChat?: boolean;
  readonly shouldTruncateChatHistory?: boolean;
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
            model: 'Gemini',
          },
          preferences: {
            displayName: 'Default Agent',
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
            shouldTruncateChatHistory: true,
          },
        },
      ],
      [
        'physics_expert',
        {
          component: PhysicsExpertComponent,
          inputs: {},
          preferences: {
            displayName: 'Physics Expert',
          },
        },
      ],
    ]);
  }
}
