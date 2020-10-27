import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Router } from '@angular/router';
import { Observable } from 'rxjs';
import { tap, shareReplay } from 'rxjs/operators';

const HttpUploadOptions = {
headers: new HttpHeaders({ "Content-Type": "multipart/form-data" })
}

@Injectable({
  providedIn: 'root'
})
export class FileService {
	private apiRoot = 'http://127.0.0.1:8000/file/';
  constructor(private http: HttpClient) { }

  postFile(fileToUpload: File) {
  	console.log("service here");
  	let headers = new Headers();
    headers.set('Accept', 'application/json');
    headers.set('Content-Type', '*/*' );
    let options = new RequestOptions({ headers: headers });
    const formData: FormData = new FormData();
    formData.append('uploaded', fileToUpload, fileToUpload.name);
    console.log(formData);
    return this.http.post<any>(this.apiRoot.concat('upload/'), formData, options);
	}
}
