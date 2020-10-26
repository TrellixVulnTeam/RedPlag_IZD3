import { Injectable } from '@angular/core';
import { HttpClient, HttpInterceptor, HttpRequest, HttpHandler, HttpEvent } from '@angular/common/http';

export interface put_data {
  first_name: string,
  last_name: string,
  phone_number: string,
}

@Injectable({
  providedIn: 'root'
})
export class AccountService {
	private url = "http://127.0.0.1:8000/api/";
  constructor(private http: HttpClient) { }
  view_profile() {
  	return this.http.get(this.url.concat('profile/'));
  }
  edit_profile(pdata: put_data) {
  	return this.http.put(this.url.concat('profile/'), JSON.stringify(pdata));
  }
  change_password(old_password: string, new_password: string) {
  	return this.http.put(this.url.concat('change_pass/'), 
  	{
	  	"old_password": old_password,
	  	"new_password": new_password
  	});
  }
  delete_user() {
  	return this.http.delete(this.url.concat('delete_user/'));
  }
}
