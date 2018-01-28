import { Component, OnInit } from '@angular/core';
import { EstadisticasService } from '../estadisticas.service';
import { MessageService } from '../message.service';
import {Message} from '../interfaces/message.interface' 

import {EstadisticaGroup} from '../interfaces/estadisticagroup.interface';

@Component({
  selector: 'app-estadisticas',
  templateUrl: './estadisticas.component.html',
  styleUrls: ['./estadisticas.component.css']
})
export class EstadisticasComponent implements OnInit {

  messageLog = new Message();

  jobListado : EstadisticaGroup[] = [];

  private doughnutChartLabels:string[] = ["a","b"];

  private doughnutChartData:number[] = [1,2];
  private doughnutChartType:string = 'doughnut';


  constructor(private estadisticasService: EstadisticasService,
  	          private messageS: MessageService ) {
  }

  ngOnInit() {
  	this.load();
  }


  // RECIBIMOS LOS DATOS DEL SERVIDOR.
  public load():void {
  	this.log("load",3,"LOG");

  	//
    this.estadisticasService.getEstadisticas("SI","pagina").subscribe(datos => {
          this.log("load",4,"get ESTADISTICAS numero: "+datos.length);
          console.log(datos);
          this.jobListado = datos;
          console.log(this.doughnutChartLabels);
	      console.log(this.doughnutChartData);
	      this.doughnutChartLabels = [];
	      this.doughnutChartData = [];
    	  this.jobListado.map(elemento => {this.doughnutChartLabels.push(elemento._id);this.doughnutChartData.push(elemento.suma)} );
    	  console.log(this.doughnutChartLabels);
    	  console.log(this.doughnutChartData);

          });
    //pasamos al drougNut:


    let _lineChartData:Array<any> = new Array(this.lineChartData.length);
    for (let i = 0; i < this.lineChartData.length; i++) {
      _lineChartData[i] = {data: new Array(this.lineChartData[i].data.length), label: this.lineChartData[i].label};
      for (let j = 0; j < this.lineChartData[i].data.length; j++) {
        _lineChartData[i].data[j] = Math.floor((Math.random() * 100) + 1);
      }
    }
    this.lineChartData = _lineChartData;
  }

    // events
  public chartClickedX(e:any):void {
    console.log(e);
  }
 
  public chartHoveredX(e:any):void {
    console.log(e);
  }



  public lineChartData:Array<any> = [
    {data: [65, 59, 80, 81, 56, 55, 40], label: 'Series A'},
    {data: [28, 48, 40, 19, 86, 27, 90], label: 'Series B'},
    {data: [18, 48, 77, 9, 100, 27, 40], label: 'Series C'}
  ];
    public lineChartLabels:Array<any> = ['January', 'February', 'March', 'April', 'May', 'June', 'July'];

  //public lineChartData:Array<any> = []



 

  public lineChartOptions:any = {
    responsive: true
  };
  public lineChartColors:Array<any> = [
    { // grey
      backgroundColor: 'rgba(148,159,177,0.2)',
      borderColor: 'rgba(148,159,177,1)',
      pointBackgroundColor: 'rgba(148,159,177,1)',
      pointBorderColor: '#fff',
      pointHoverBackgroundColor: '#fff',
      pointHoverBorderColor: 'rgba(148,159,177,0.8)'
    },
    { // dark grey
      backgroundColor: 'rgba(77,83,96,0.2)',
      borderColor: 'rgba(77,83,96,1)',
      pointBackgroundColor: 'rgba(77,83,96,1)',
      pointBorderColor: '#fff',
      pointHoverBackgroundColor: '#fff',
      pointHoverBorderColor: 'rgba(77,83,96,1)'
    },
    { // grey
      backgroundColor: 'rgba(148,159,177,0.2)',
      borderColor: 'rgba(148,159,177,1)',
      pointBackgroundColor: 'rgba(148,159,177,1)',
      pointBorderColor: '#fff',
      pointHoverBackgroundColor: '#fff',
      pointHoverBorderColor: 'rgba(148,159,177,0.8)'
    }
  ];
  public lineChartLegend:boolean = true;
  public lineChartType:string = 'line';
 
 
  // events
  public chartClicked(e:any):void {
    console.log(e);
  }
 
  public chartHovered(e:any):void {
    console.log(e);
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
