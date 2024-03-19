// Represents a message in a conversation.
export interface ChatMessage {
  author: string;
  content: string;
}

// Controls the model and prompt used in a conversation.
// TODO: Prettify display strings in the menu.
export type PromptMode = 'default' | 'fake' | 'history_tutor';
