import { Injectable } from '@angular/core';
import { HttpClient, HttpRequest, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { tap, shareReplay } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class GraphServiceService {
	private apiRoot = 'http://127.0.0.1:8000/file/';
  constructor(private http: HttpClient) { }
  getHistogram() {
  console.log("histogram service");
  const httpOptions = {
    responseType: 'blob' as 'json',
	};
	return this.http.get(this.apiRoot.concat('histogram/'), httpOptions);
  }
}
