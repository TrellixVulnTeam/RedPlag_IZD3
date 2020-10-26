import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AccountService } from '../account.service';

@Component({
  selector: 'app-edit-profile',
  templateUrl: './edit-profile.component.html',
  styleUrls: ['./edit-profile.component.scss']
})
export class EditProfileComponent implements OnInit {
		profileForm = this.fb.group({
    first_name: ['', Validators.required],
    last_name: ['', Validators.required],
    phone_no: ['', Validators.required],
  });
  constructor(private fb: FormBuilder, private accountService: AccountService ) { }

  ngOnInit(): void {
  }
  onSubmit() {
    this.accountService.edit_profile(this.profileForm.value).subscribe(
      success => console.log(success),
      error => console.log(error)
    )
  }
}
