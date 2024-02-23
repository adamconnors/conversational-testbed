import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ChatService {

  private apiUrl = `${environment.apiUrl}/chat`;

  constructor(private http: HttpClient) { }

  getLLMLineOfDialog(request: string, message_history: string[]): Observable<string> {
    const formData = new FormData();
    formData.append('q', request);
    formData.append('message_history', JSON.stringify(message_history))
    return this.http.post(this.apiUrl, formData, { responseType: 'text' });
  }
}
