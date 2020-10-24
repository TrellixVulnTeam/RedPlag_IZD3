import { Component, OnInit } from '@angular/core';
import { FormBuilder, Validators, EmailValidator} from '@angular/forms';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
	profileForm = this.fb.group({
    email: ['', Validators.pattern("^[a-z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,4}$")],
    password: ['',Validators.required],
  });
  constructor(private fb: FormBuilder) {};

  ngOnInit(): void {};
  onSubmit() {

  }

}
