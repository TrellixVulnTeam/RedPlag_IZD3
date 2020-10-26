import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import { ReactiveFormsModule } from '@angular/forms';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LoginComponent } from './login/login.component';
import { SignupComponent } from './signup/signup.component';
import { MyAccountComponent } from './my-account/my-account.component';
import { ViewProfileComponent } from './view-profile/view-profile.component';
import { EditProfileComponent } from './edit-profile/edit-profile.component';
import { PasswordDeleteComponent } from './password-delete/password-delete.component';
import { HeaderComponent } from './header/header.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { AuthService, AuthInterceptor, AuthGuard } from './auth.service';
import { AuthErrorHandler } from './auth-error-handler';
import { ErrorHandler, Injectable, Injector } from '@angular/core';
import { RedPlagComponent } from './red-plag/red-plag.component';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    SignupComponent,
    MyAccountComponent,
    ViewProfileComponent,
    EditProfileComponent,
    PasswordDeleteComponent,
    HeaderComponent,
    DashboardComponent,
    RedPlagComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    ReactiveFormsModule,
    HttpClientModule,
    RouterModule,
  ],
  providers: [
    AuthService,
    AuthGuard,
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthInterceptor,
      multi: true,
    },
    {
      provide: ErrorHandler, 
      useClass: AuthErrorHandler,
    },
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
