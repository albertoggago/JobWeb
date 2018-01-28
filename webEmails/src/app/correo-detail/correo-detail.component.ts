import { Component, Input, OnChanges, EventEmitter, Output, NgZone} from '@angular/core';
import { NgForOf } from '@angular/common';
import { MessageService } from '../message.service';

import {Correo} from '../interfaces/correo.interface' 
import {Modelo} from '../interfaces/modelo.interface'
import {Message} from '../interfaces/message.interface' 
import 'rxjs/add/operator/toPromise';
 

import { GMapsService } from '../gmaps.service';
import { CorreosService } from '../correos.service';
  
@Component({
  selector: 'app-correo-detail',
  templateUrl: './correo-detail.component.html', 
  styleUrls: ['./correo-detail.component.css']
})
export class CorreoDetailComponent implements OnChanges {
  @Input() correo: Correo;
  
  @Output('update') 
  guardadoH : EventEmitter<number> = new EventEmitter<number> ();
 
  modelos : Modelo[];
  messageLog = new Message();

 decisiones : any [] = [{"value":"SI","display":"SI"},
                        {"value":"NO","display":"NO"}];

  lat: number = 42;
  lng: number = 0.809007;
 

  constructor(
		private messageS: MessageService,
    private correosService: CorreosService,
    private gMapsService: GMapsService, 
    private __zone: NgZone
      	) { 
    this.initLog();
  }

  ngOnInit() {
  }


  ngOnChanges(){
    this.log("ngOnChanges",3,"LOG");

    if (this.correo !== undefined)
    {
      this.correo.summary = this.correo.summary.split("\n").join("<br>");
      this.correo.urlDonde = "https://www.google.es/maps/place/"+this.correo.donde.split(" ").join("+");

      this.log("ngOnChanges",4,"urlDonde: "+this.correo.urlDonde);

      this.modelos = [];
      for (var i=0; i< this.correo.modelos.length;i++){
        var mod = this.correo.modelos[i];
        var modelo = new Modelo();

        var x = 0;
        if (mod.decisionPRED=="SI")
          {x = mod.porcentPRED/2+50;}
        else
          {x = 50-mod.porcentPRED/2;}
        x = Math.round(x)
        modelo.valorSI = x+"%";
        modelo.valorNO = (100-x)+"%";
        modelo.nombre = mod.modelo;
        this.modelos.push(modelo);
      }

      //buscar lat long
      this.getAddress();
    }

  }

  onGuardar() {
    this.log("onGuardar",3,"LOG");
    
    this.log("onGuardar",3,"Enviar Correo Guardado: "+this.correo.numeroCorreo);
    this.guardadoH.emit(this.correo.numeroCorreo);
    if (this.correo.isSended) {
        window.open(this.correo.urlOk, "_blank");
    }
    this.correosService.setCorreo(this.correo)
        .subscribe(resultado => {
             this.log("onGuardar",4,"resultado: "+resultado);
             });
  };

  isSendedValid(){
    //this.log("isSendedValid",3,"LOG");
    return (this.correo.decision == "SI");
  }

  isFormValid(){
    //this.log("isFormValid",3,"LOG");
    if (this.correo != undefined) {
      return ((this.correo.observaciones != undefined) && !(this.correo.decision ==  null));
    }
    else {return false;}
  }



  onSiNo(valor:string) {
    this.log("onSiNo",3,"LOG");
    this.log("onSiNo",3,"onSINO : "+valor);

    this.correo.decision = valor;
    if (valor == "SI" ) {
      this.correo.isSended = true;
    } else
      this.correo.isSended = false;
    if (this.correo.observaciones == null) {
      this.correo.observaciones = this.correo.titulo;
    }
  }


  getAddress() {
    this.log("getAddress",3,"LOG");
    const donde = this.correo.donde.split("/")[0].split(",")[0];
    //console.log(donde);
    this.gMapsService.getLatLan(donde+" Ireland")
          .subscribe(resultado => {
             this.log("getAddress",4,"resultado: "+resultado);
             //console.log(resultado.results[0].geometry.location);
             this.lat = resultado.results[0].geometry.location.lat;
             this.lng = resultado.results[0].geometry.location.lng;

             });
  }

  private initLog() {
    this.messageLog.where ="correo-detail";
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

