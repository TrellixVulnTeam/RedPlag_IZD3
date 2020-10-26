import { Injectable } from '@angular/core';
import { HttpClient, HttpInterceptor, HttpRequest, HttpHandler, HttpEvent, HttpHeaders } from '@angular/common/http';
import { map, tap } from 'rxjs/operators';

export interface put_data {
  first_name: string,
  last_name: string,
  phone_number: string,
  age: number,
  gender: string
}

@Injectable({
  providedIn: 'root'
})
export class AccountService {
	private url = "http://127.0.0.1:8000/api/";
	httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
  };
  constructor(private http: HttpClient) { }
  view_profile() {
  	return this.http.get<any>(this.url.concat('profile/'));
  }
  edit_profile(pdata: put_data) {
  	console.log(JSON.stringify(pdata));
  	return this.http.put(this.url.concat('profile/'), JSON.stringify(pdata), this.httpOptions).pipe(tap((data) => console.log("successful")));
  }
  change_password(old_password: string, new_password: string) {
  	return this.http.put(this.url.concat('change_pass/'), 
  	{
	  	"old_password": old_password,
	  	"new_password": new_password
  	}, this.httpOptions).pipe(tap((data) => console.log("successful")));
  }
  delete_user() {
  	return this.http.delete(this.url.concat('delete_user/'));
  }
}
