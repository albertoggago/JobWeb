import { Component, OnInit } from '@angular/core';
import {AuthenticationService} from '../authentication.service'
import { MessageService } from '../message.service';

import {User} from '../interfaces/user.interface'
import {Message} from '../interfaces/message.interface'
import { GMapsService } from '../gmaps.service';

@Component({
  selector: 'app-authentication',
  templateUrl: './authentication.component.html',
  styleUrls: ['./authentication.component.css']
})
export class AuthenticationComponent implements OnInit {

  user : User = new User();
  
  messageLog = new Message();

  constructor(
  private _service:AuthenticationService,
  private messageS: MessageService,
  private gmapsService : GMapsService
  	) { 
    this.initLog();
  }

  ngOnInit() {
   
  }

  login() {

    this.log("login",3,"user: "+this.user.email);
    this._service.login(this.user,"lista",0);
  }

  private initLog() {
    this.messageLog.where ="authentication";
    this.messageLog.tipo  = "component";
    this.messageLog.funcion = "constructor";
    this.messageLog.level = 3;
    this.messageLog.texto = "LOG";
    this.messageS.add(this.messageLog);
  }

  private log(funcion: string, level:number, texto: string) {
    this.messageLog.funcion = funcion;
    this.messageLog.level = level;
    this.messageLog.texto = texto;
    this.messageS.add(this.messageLog);
  }



}


