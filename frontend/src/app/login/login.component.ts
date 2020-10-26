import { Component, OnInit } from '@angular/core';
import { FormBuilder, Validators, EmailValidator} from '@angular/forms';
import { AuthService } from '../auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {
	profileForm = this.fb.group({
    email: ['', Validators.pattern("^[a-z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,4}$")],
    password: ['',Validators.required],
  });
  error: any;
  constructor(private fb: FormBuilder, private authService: AuthService, private router: Router) {};

  ngOnInit(): void {};
  onSubmit() {
    this.login(this.profileForm.value.email, this.profileForm.value.password)
  }
  login(email: string, password: string) {
    this.authService.login(email, password).subscribe(
      success => {this.router.navigate(['/dashboard']);
      console.log("success");},
      error => this.error = error
    );
  }

}
