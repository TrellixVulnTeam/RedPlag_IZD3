import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { first } from 'rxjs/operators';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent implements OnInit {
	profileForm = this.fb.group({
    firstName: ['', Validators.required],
    lastName: ['', Validators.required],
    email: ['', Validators.required],
    password: ['', [Validators.required, Validators.minLength(8)]],
    phone_no: ['', Validators.required],
    age: ['', Validators.required],
    gender: ['', Validators.required],
  });
  loading = false;
  submitted = false;

  constructor(private fb: FormBuilder) {};

  ngOnInit(): void {};
  onSubmit() {

  }

}
