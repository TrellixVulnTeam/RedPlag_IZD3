import { Injectable } from '@angular/core';
import { HttpClient, HttpInterceptor, HttpRequest, HttpHandler, HttpEvent } from '@angular/common/http';
import { CanActivate, Router } from '@angular/router';

import { Observable } from 'rxjs';
import { tap, shareReplay } from 'rxjs/operators';

import jwt_decode from 'jwt-decode';
import * as moment from 'moment';

import { environment } from '../environments/environment';

export interface signup_data {
  email: string,
  password: string,
  first_name: string,
  last_name: string,
  phone_number: string,
}

@Injectable({
    providedIn: 'root'
})
export class AuthService {

  private apiRoot = 'http://127.0.0.1:8000/api/';
  token;
  constructor(private http: HttpClient) { }

  private setSession(authResult) {
    const token = authResult.token;
    console.log(token);
    const payload = <JWTPayload> jwt_decode(token);
    console.log(jwt_decode(token));
    const expiresAt = moment.unix(payload.exp);
    localStorage.setItem('token', authResult.token);
    localStorage.setItem('expires_at', JSON.stringify(expiresAt.valueOf()));
    console.log(JSON.stringify(expiresAt.valueOf()));
    console.log(authResult.token);
  }

  get_token(): string {
    return localStorage.getItem('token');
  }

  login(email: string, password: string) {
  let token =
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL2V4YW1wbGUuY29tLyIsInN1YiI6ImF1dGgwfGFiYzEyMyIsImF1ZCI6ImNsaWVudElkIiwiaWF0IjoxNTY4MDk2MDQyLCJleHAiOjIwNzMzNDY3Mzh9.lMKzXXCdQA3uFP5ONh1LrmKF0NouRh-Ys-q_aFeN1Ek";
  console.log("hello");
let decoded = jwt_decode(token);
console.log("hi");
console.log(decoded);

    return this.http.post(
      this.apiRoot.concat('login/'),
      { "email":email, "password":password }
    ).pipe(
      tap(response => this.setSession(response)),
      shareReplay(),
    );
  }

  signup(sdata: signup_data) {
    return this.http.post(
      this.apiRoot.concat('signup/'),
      {
      "email":sdata.email,
      "password":sdata.password,
      "profile": {
             "first_name": sdata.first_name,
             "last_name": sdata.last_name,
             "phone_number": sdata.phone_number,
             "age": 11,
             "gender": "M"
      }
      }
    );
  }

  logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('expires_at');
  }

  // refreshToken() {
  //   if (moment().isBetween(this.getExpiration().subtract(1, 'hours'), this.getExpiration())) {
  //    return this.http.post(
  //      this.apiRoot.concat('refresh-token/'),
  //      { token: this.token }
  //    ).pipe(
  //      tap(response => this.setSession(response)),
  //      shareReplay(),
  //    ).subscribe();
  //   }
  // }

  getExpiration() {
    const expiration = localStorage.getItem('expires_at');
    const expiresAt = JSON.parse(expiration);

    return moment(expiresAt);
  }

  isLoggedIn() {
    return moment().isBefore(this.getExpiration());
  }

  isLoggedOut() {
    return !this.isLoggedIn();
  }
}

@Injectable()
export class AuthInterceptor implements HttpInterceptor {

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    const token = localStorage.getItem('token');
    console.log("how are you");
    console.log(token);
    if (token) {
      const cloned = req.clone({
        headers: req.headers.set('Authorization', 'Bearer '.concat(token))
      });

      return next.handle(cloned);
    } else {
      return next.handle(req);
    }
  }
}

@Injectable()
export class AuthGuard implements CanActivate {

  constructor(private authService: AuthService, private router: Router) { }

  canActivate() {
    if (this.authService.isLoggedIn()) {
      // this.authService.refreshToken();

      return true;
    } else {
      this.authService.logout();
      this.router.navigate(['login/']);

      return false;
    }
  }
}

interface JWTPayload {
  user_id: number;
  username: string;
  exp: number;
  email: string;
}