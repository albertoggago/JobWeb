import { NgModule }             from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
 
import { CorreosComponent }   from '../correos/correos.component';
import { CorreoDetailComponent }   from '../correo-detail/correo-detail.component';
import { AuthenticationComponent }      from '../authentication/authentication.component';
import { DashboardComponent }      from '../dashboard/dashboard.component';
import { EstadisticasComponent }      from '../estadisticas/estadisticas.component';

 
const routes: Routes = [
  { path: '', redirectTo: '/lista', pathMatch: 'full' },
  { path: 'dashboard', component: DashboardComponent },
  { path: 'auth', component: AuthenticationComponent },
  { path: 'lista', component: CorreosComponent },
  { path: 'detalle/:id', component: CorreoDetailComponent },
  { path: 'estadisticas', component: EstadisticasComponent },
];
 
@NgModule({
  imports: [ RouterModule.forRoot(routes) ],
  exports: [ RouterModule ]
})
export class AppRoutingModule {}