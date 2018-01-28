import { Component, OnInit } from '@angular/core';
import { MessageService } from '../message.service';
import {Message} from '../interfaces/message.interface';
import { Pipe } from '@angular/core';


@Component({
  selector: 'app-message', 
  templateUrl: './message.component.html',
  styleUrls: ['./message.component.css']
})
export class MessageComponent implements OnInit {

  constructor(public messageService: MessageService) {}

//LEVELS
  // 0 FATAL / SEVERE
  // 1 ERROR
  // 2 WARNING
  // 3 INFO
  // 4 DEBUG
  // 5 TRACE
levels = ["FATAL","ERROR","WARNING","INFO", "DEBUG", "TRACE"]



  getTextLevel(level:number){
    return this.levels[level];
  }


  ngOnInit() {
  }


}
