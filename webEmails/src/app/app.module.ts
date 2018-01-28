import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';  
 
import { AppRoutingModule }     from './app-routing/app-routing.module'; 

import { AgmCoreModule } from '@agm/core';

import { AppComponent } from './app.component';
import { CorreosComponent } from './correos/correos.component';
import { CorreoDetailComponent } from './correo-detail/correo-detail.component';
import { MessageComponent } from './message/message.component';
import { AuthenticationComponent } from './authentication/authentication.component';
import { DashboardComponent }      from './dashboard/dashboard.component';
import { EstadisticasComponent }      from './estadisticas/estadisticas.component';

import { AuthenticationService } from './authentication.service';
import { MessageService } from './message.service'; 
import { CorreosService } from './correos.service';
import { GMapsService } from './gmaps.service';
import { EstadisticasService } from './estadisticas.service';
import { GeneralService } from './general.service';

import { ChartsModule } from 'ng2-charts';

 

 
@NgModule({
  declarations: [
    AppComponent,
    CorreosComponent,
    CorreoDetailComponent,
    MessageComponent,
    AuthenticationComponent,
    DashboardComponent, 
    EstadisticasComponent
  ],
  imports: [
    AppRoutingModule,
    BrowserModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
    ChartsModule,
    AgmCoreModule.forRoot({
      apiKey: 'AIzaSyAs3JCBHNrrurTXN6yK4t3ceg69iM6attY'
    })
  ],
  providers: [AuthenticationService, MessageService, CorreosService, GMapsService, EstadisticasService,GeneralService],
  bootstrap: [AppComponent]
})
export class AppModule { }
