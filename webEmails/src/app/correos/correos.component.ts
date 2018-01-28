import { Component, OnInit, Inject   }  from '@angular/core';
import { FormGroup, FormBuilder, Validators, FormControl } from '@angular/forms';

import { AgmCoreModule } from '@agm/core';

import {AuthenticationService} from '../authentication.service'
import { CorreoDetailComponent } from '../correo-detail/correo-detail.component';
import { MessageService } from '../message.service';
import { CorreosService } from '../correos.service';

import {Correo} from '../interfaces/correo.interface'
import {Message} from '../interfaces/message.interface' 


@Component({
  selector: 'app-correos',
  templateUrl: './correos.component.html',
  styleUrls: ['./correos.component.css']
})
export class CorreosComponent implements OnInit {

correos : Correo[];
selectedCorreo : Correo;
messageLog = new Message();

public selecciones = [
    { value: "A", display:"Pendientes" },
    { value: "B", display:"Mejores NO" },
    { value: "C", display:"Peores SI" },
    { value: "D", display:"Ya Enviado" },
    { value: "E", display:"Marcado SI" },
    { value: "F", display:"Marcado NO" },
    
    { value: "J", display:"Texto" }
  ];
tipoListado : FormGroup;


//variables para la navegacion
tipoSearch : string = this.selecciones[0].value;
palabrasOld: string = "";
seleccionado: number = 0;
cantidad: number = 0;

    constructor(
//	private route: ActivatedRouteSnapshot,
//  	private location: Location
		private fb: FormBuilder,
		private authenticationService:AuthenticationService,
		private messageS: MessageService,
		private correosService: CorreosService
		//private correoDetailComponent: CorreoDetailComponent
		//
		) { 
    	this.tipoListado = fb.group({
     		"seleccion": this.selecciones[0],
     		"palabras": '' 
    	});
    this.initLog();
  	}

  ngOnInit() {
  	this.authenticationService.checkCredentials("lista");
    this.correosService.getAllCorreos(this.selecciones[0].value, 0, "")
       .subscribe(elementos => {
          this.correos = elementos;
          this.tipoSearch = this.selecciones[0].value;
          this.cantidad = this.correos.length;
          if (this.correos.length>0) {
		  	    this.renumerarCorreos();
            this.seleccionado = 0;
            this.onSelect(this.correos[this.seleccionado]);
          }
      	}
  	)}

  onSelect(correo: Correo): void {
      this.log("onSelect",3,"LOG");
      this.log("onSelect",4,"Titulo: "+ correo.titulo);

    	this.selectedCorreo = correo;
    	this.seleccionado = this.selectedCorreo.numeroCorreo;
	};

  onRefrescarBusqueda(tipoL:any, final:boolean) {
    this.log("onRefrescarBusqueda",3,"LOG");
    this.log("onRefrescarBusqueda",4,"tipoL: "+tipoL);
    this.log("onRefrescarBusqueda",4,"final: "+final.toString());
    const palabras = tipoL.controls.palabras.value;
    const seleccion = tipoL.controls.seleccion.value.value;
    let posicionamiento = true;
    let   cantidadTemp = 0;
    this.log("onRefrescarBusqueda",4,"palabras: "+palabras);
    this.log("onRefrescarBusqueda",4,"seleccion: "+seleccion);
    if (this.tipoSearch== seleccion && seleccion != "J") {
	    cantidadTemp = this.cantidad;
    } else if (this.palabrasOld == palabras && seleccion == "J"){
      cantidadTemp = this.cantidad;
    } else{
      this.correos = [];
  	  this.tipoSearch=seleccion;
     	this.palabrasOld = palabras;
      posicionamiento = false;
      this.seleccionado = null;
      this.selectedCorreo = null;
    };

    this.correosService.getAllCorreos(seleccion,cantidadTemp,palabras).subscribe(datos => {
          this.log("onRefrescarBusqueda",4,"seleccion: "+"HTTP call numero: "+datos.length);
          datos.map(elemento => this.correos.push(elemento) );
          this.cantidad = this.correos.length;
          if (this.cantidad>0) {
            //
            this.renumerarCorreos();
            this.log("onRefrescarBusqueda",4,"Reestructurar la busqueda");
            if (!posicionamiento) {
              this.seleccionado = 0;  
            } else if (final && datos.length>0) {
              this.seleccionado += 1;
            };
            this.onSelect(this.correos[this.seleccionado]);
          } 
          })
  }
  
  renumerarCorreos(){
    this.log("renumerarCorreos",3,"LOG");
      for (var i=0;i< this.correos.length;i++){
        this.correos[i].numeroCorreo = i;
      }
  }

  onBajar(){
    this.log("onBajar",3,"LOG");
    if (this.selectedCorreo.numeroCorreo < (this.correos.length-1)) {
      this.onSelect(this.correos[this.selectedCorreo.numeroCorreo+1]);
    } else if (this.seleccionado > 0) {
      this.onRefrescarBusqueda(this.tipoListado, true);
    }
  }

  onSubir(){
    this.log("onSubir",3,"LOG");
    if (this.selectedCorreo.numeroCorreo > 0) {
      this.onSelect(this.correos[this.selectedCorreo.numeroCorreo-1]);
    }
  }

  guardadoP(correoGuardado: number) {
    this.log("guardadoP",3,"LOG");
    this.log("guardadoP",4,"correoGuardado "+correoGuardado);
    //realizamos las acciones de
    this.onBajar()
    //reiniciamos la busqueda para que el sistema si doy buscar limpie.
    this.tipoSearch = "CAMBIAR XX YY XX";
  }

  onLogOut(){
    this.log("onLogOut",3,"LOG");
    this.authenticationService.goAuthPage();

  }


  private initLog() {
    this.messageLog.where ="correos";
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


