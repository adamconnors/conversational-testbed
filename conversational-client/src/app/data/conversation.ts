// Represents a message in a conversation.
export interface ChatMessage {
  author: string;
  content: string;
}

// Controls the model and prompt used in a conversation.
export type PromptMode = 'default' | 'fake';
