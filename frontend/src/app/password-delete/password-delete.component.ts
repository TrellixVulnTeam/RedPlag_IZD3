import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AccountService } from '../account.service';

@Component({
  selector: 'app-password-delete',
  templateUrl: './password-delete.component.html',
  styleUrls: ['./password-delete.component.scss']
})
export class PasswordDeleteComponent implements OnInit {
	profileForm = this.fb.group({
    old_password: ['', [Validators.required, Validators.minLength(8)]],
    new_password1: ['', [Validators.required, Validators.minLength(8)]],
    new_password: ['', [Validators.required, Validators.minLength(8)]],
  });
  constructor(private fb: FormBuilder, private accountService: AccountService) { }

  ngOnInit(): void {
  }
  updateData() {
    console.log(this.profileForm.value.old_password);
    console.log(this.profileForm.value.new_password);
    this.accountService.change_password(this.profileForm.value.old_password, this.profileForm.value.new_password).subscribe(
      success => console.log(success),
      error => console.log(error)
    )
  }
  deleteUser() {
    this.accountService.delete_user().subscribe(
      success => console.log(success),
      error => console.log(error)
    )
  }
}
