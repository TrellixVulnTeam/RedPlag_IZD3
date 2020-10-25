import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-password-delete',
  templateUrl: './password-delete.component.html',
  styleUrls: ['./password-delete.component.scss']
})
export class PasswordDeleteComponent implements OnInit {
	profileForm = this.fb.group({
    old_password: ['', [Validators.required, Validators.minLength(8)]],
    new_password1: ['', [Validators.required, Validators.minLength(8)]],
    new_password2: ['', [Validators.required, Validators.minLength(8)]],
  });
  constructor(private fb: FormBuilder) { }

  ngOnInit(): void {
  }
  onSubmit() {
  
  }
}
