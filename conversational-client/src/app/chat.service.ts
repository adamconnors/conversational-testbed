import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ChatService {

  // backendURL = "http://localhost:8080/chat";
  backendURL = "/chat";

  constructor(private http: HttpClient) { }

  getLLMLineOfDialog(request: string, message_history: string[]): Observable<string> {
    const url = this.backendURL;
    const formData = new FormData();
    formData.append('q', request);
    formData.append('message_history', JSON.stringify(message_history))
    return this.http.post(url, formData, { responseType: 'text' });
  }
}
