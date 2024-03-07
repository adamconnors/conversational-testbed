import {HttpClient} from '@angular/common/http';
import {Injectable} from '@angular/core';
import {Observable} from 'rxjs';
import {environment} from 'environments/environment';

@Injectable({
  providedIn: 'root',
})
export class ChatService {
  private apiUrl = `${environment.apiUrl}/chat`;

  constructor(private http: HttpClient) {}

  getLLMLineOfDialog(
    request: string,
    messageHistory: string[]
  ): Observable<string> {
    const formData = new FormData();
    formData.append('q', request);
    formData.append('message_history', JSON.stringify(messageHistory));
    return this.http.post(this.apiUrl, formData, {responseType: 'text'});
  }

  downloadTranscript(messageHistory: string[]) {
    const transcript = messageHistory
      .map((s, i) => `${i % 2 === 0 ? '<me>' : '<llm>'}${s.trim()}</end>`)
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
