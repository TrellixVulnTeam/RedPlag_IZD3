import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { first } from 'rxjs/operators';
import { AuthService } from '../auth.service';
import { AlertService } from '../alert.service';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.scss']
})
export class SignupComponent implements OnInit {
  error: any;
	profileForm = this.fb.group({
    email: ['', Validators.required],
    password: ['', [Validators.required, Validators.minLength(8)]],
    rePassword: ['', [Validators.required, Validators.minLength(8)]],
    first_name: ['', Validators.required],
    last_name: ['', Validators.required],
    phone_number: ['', Validators.required],
  });

  constructor(private fb: FormBuilder, private authService: AuthService, private router: Router, private alertService: AlertService) {};

  ngOnInit(): void {};
  onSubmit() {
    this.alertService.clear();
//    console.log(this.profileForm.value.password);
//    if(this.profileForm.value.password!=this.profileForm.value.rePassword) {
//      this.alert("this.profileForm.password")
//      this.alertService.error("Passwords Don't match");
//      return;
//    }
    this.authService.signup(this.profileForm.value).subscribe(
      success => {console.log(success);
      this.router.navigate(['/login']);},
      error => this.error = error
    );
  }

}
