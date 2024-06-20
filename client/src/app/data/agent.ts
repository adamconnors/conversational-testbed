// Identifies the agent used in a conversation.
// Add new agents here. The agent ID must match the agent_id defined
// in server/agents/registry.py
export const AGENT_IDS = [
  'default',
  'fake',
  'history_tutor',
  'physics_expert',
] as const;
export type AgentId = (typeof AGENT_IDS)[number];

// Represents a stateful conversational agent.
export interface Agent {
  // Updates the agent state following a conversation exchange.
  processExchange(state: AgentState): AgentState;
}

// Represents a generic agent state.
export interface AgentState {
  messageHistory: ChatMessage[];
  worldState: unknown | null;
}

// Represents a message in a conversation.
export interface ChatMessage {
  author: 'human' | 'ai';
  content: string;
}
