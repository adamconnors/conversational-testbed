// Represents a message in a conversation.
export interface ChatMessage {
  author: string;
  content: string;
}

// Controls the agent used in a conversation.
export const AGENT_IDS = ['default', 'fake', 'history_tutor'] as const;
export type AgentId = (typeof AGENT_IDS)[number];
