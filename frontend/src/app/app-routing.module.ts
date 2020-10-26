import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { SignupComponent } from './signup/signup.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { MyAccountComponent } from './my-account/my-account.component';
import { ViewProfileComponent } from './view-profile/view-profile.component';
import { EditProfileComponent } from './edit-profile/edit-profile.component';
import { PasswordDeleteComponent } from './password-delete/password-delete.component';
import { AuthGuard } from './auth.service';
import { RedPlagComponent } from './red-plag/red-plag.component';

const routes: Routes = [
	{ path: '', redirectTo: '/login', pathMatch: 'full' },
	{ path: 'login', component: LoginComponent },
	{ path: 'signup', component: SignupComponent },
	{ path: 'dashboard', component: DashboardComponent, canActivate: [AuthGuard],
		children: [
      {
        path: 'account',
        component: MyAccountComponent,
        children: [
		      {
		        path: 'profile',
		        component: ViewProfileComponent,
		        canActivate: [AuthGuard],
		      },
		      {
		        path: 'edit_profile',
		        component: EditProfileComponent,
		        canActivate: [AuthGuard],
		      },
		      {
		      	path: 'security',
		      	component: PasswordDeleteComponent,
		      	canActivate: [AuthGuard],
		      },
		      {
		      	path: '', redirectTo: '/dashboard/account/profile', pathMatch: 'full',
		      },
		    ],
      },
      {
      	path: 'red_plag',
        component: RedPlagComponent,
        canActivate: [AuthGuard],
      }
    ],
	},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
