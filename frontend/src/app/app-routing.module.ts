import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { SignupComponent } from './signup/signup.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { MyAccountComponent } from './my-account/my-account.component';
import { ViewProfileComponent } from './view-profile/view-profile.component';
import { EditProfileComponent } from './edit-profile/edit-profile.component';
import { PasswordDeleteComponent } from './password-delete/password-delete.component';

const routes: Routes = [
	{ path: '', redirectTo: '/login', pathMatch: 'full' },
	{ path: 'login', component: LoginComponent },
	{ path: 'signup', component: SignupComponent },
	{ path: 'dashboard', component: DashboardComponent,
		children: [
      {
        path: 'account',
        component: MyAccountComponent,
        children: [
		      {
		        path: 'profile',
		        component: ViewProfileComponent,
		      },
		      {
		        path: 'edit_profile',
		        component: EditProfileComponent,
		      },
		      {
		      	path: 'actions',
		      	component: PasswordDeleteComponent,
		      }
		    ],
      },
    ],
	},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
