import {HttpClient} from '@angular/common/http';
import {Injectable} from '@angular/core';
import {Observable} from 'rxjs';
import {ChatMessage, PromptMode} from 'app/data/conversation';
import {environment} from 'environments/environment';

@Injectable({
  providedIn: 'root',
})
export class ChatService {
  private apiUrl = `${environment.apiUrl}/chat`;

  constructor(private http: HttpClient) {}

  sendMessage(
    request: string,
    messageHistory: ChatMessage[],
    worldState: object,
    promptMode: PromptMode
  ): Observable<string> {
    const formData = new FormData();
    formData.append('q', request);
    formData.append('message_history', JSON.stringify(messageHistory));
    formData.append('world_state', JSON.stringify(worldState));
    formData.append('mode', promptMode);
    return this.http.post(this.apiUrl, formData, {responseType: 'text'});
  }

  downloadTranscript(messageHistory: ChatMessage[]) {
    const transcript = messageHistory
      .map(msg => `<${msg.author}>${msg.content}</${msg.author}>`)
      .join('\n\n');
    const filename = `chat_transcript-${Date.now()}.txt`;
    this.downloadFile(transcript, filename, 'text/plain');
  }

  private downloadFile(data: string, filename: string, type: string) {
    const blob = new Blob([data], {type: type});
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    link.click(); // Trigger the download
    window.URL.revokeObjectURL(url); // Clean up
  }
}
