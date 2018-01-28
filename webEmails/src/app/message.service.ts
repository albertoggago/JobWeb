import { Injectable } from '@angular/core';
import {Message} from './interfaces/message.interface'

@Injectable()
export class MessageService {
  messages: Message[] = []; 
  maximo : number = 50;

  add(message : Message) {
    let messageNew = new Message();
    messageNew.tipo = message.tipo;
    messageNew.where = message.where;
    messageNew.funcion = message.funcion;
    messageNew.level = message.level;
    messageNew.texto  = message.texto;

    messageNew.fecha = new Date();
  	this.messages.push(messageNew);
    if (this.messages.length > this.maximo ){
      this.messages.splice(0,this.messages.length-this.maximo);
    }
  }

  //LEVELS
  // 0 FATAL / SEVERE
  // 1 ERROR
  // 2 WARNING
  // 3 INFO
  // 4 DEBUG
  // 5 TRACE


  clear() {
    this.messages = [];
  }
}