import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class APIService {

  backendURL = "http://localhost:8080/api";
  // backendURL = "/api";

  constructor(private http: HttpClient) { }

  getLLMLineOfDialog(request: string): Observable<string> {
    const url = this.backendURL;
    const formData = new FormData();
    formData.append('q', request);
    return this.http.post(url, formData, { responseType: 'text' });
  }
}
