import { Component, OnInit } from '@angular/core';
import { AccountService } from '../account.service';

@Component({
  selector: 'app-view-profile',
  templateUrl: './view-profile.component.html',
  styleUrls: ['./view-profile.component.scss']
})

export class ViewProfileComponent implements OnInit {
	first_name: string;
	last_name: string;
	phone_no: string;
  constructor(private accountService: AccountService) {}

  ngOnInit(): void {
  	this.accountService.view_profile().subscribe(
  		success => console.log(success),
  		error => console.log(error)
  	)
  }

}
