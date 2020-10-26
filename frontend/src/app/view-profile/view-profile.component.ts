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
	phone_no: string = "198273";
  constructor(private accountService: AccountService) {}

  ngOnInit(): void {
  	this.accountService.view_profile().subscribe(
  		response => {
        var obt_data = JSON.parse(JSON.stringify(response));
        console.log(obt_data.data);
        this.first_name = obt_data.data.first_name;
        this.last_name = obt_data.data.last_name;
        this.phone_no = obt_data.data.phone_number;
      },
  		error => console.log(error)
  	)
  }
}
