import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs/Observable'; 
import { of } from 'rxjs/observable/of';
import { catchError, tap } from 'rxjs/operators';

import { MessageService } from './message.service';
import { GeneralService } from './general.service';

import {Message} from './interfaces/message.interface';
import {EstadisticaGroup} from './interfaces/estadisticagroup.interface';

const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json' })
};


@Injectable()
export class EstadisticasService {

  messageLog = new Message();

  private Path: String = "";

  constructor(private http: HttpClient,
  	          private messageS: MessageService,
              private general: GeneralService
  	          ) { 
            this.Path = general.getPathBase();
          }

  

  //router.route('/correourls/decision/:decision/grupo/:grupo')
  getEstadisticas(decision:string, grupo:string): Observable<EstadisticaGroup[]> {
      this.log("getEstadisticas",3,"LOG");
      this.log("getEstadisticas",4,"Decision: "+decision+" , grupo: "+grupo);
   		if (decision == "") {decision = "VOID";}
    	const url = this.Path+'/correourls/decision/'+decision+'/grupo/'+grupo;
    	return this.http.get<EstadisticaGroup[]>(url)
    		.pipe(
          	tap( estadisticaGroup => this.log("getAllCorreos",5, 'fetched correos : '+estadisticaGroup)),
        	catchError(this.handleError('Error buscando correos valor ${valor}',[]))
            );
  }



  private handleError<T> (operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {

      // TODO: send the error to remote logging infrastructure
      console.error(error); // log to console instead

      // TODO: better job of transforming error for user consumption
      this.log("setCorreos",1,`${operation} failed: ${error.message}`);

      // Let the app keep running by returning an empty result.
      return of(result as T);
    };
  }

  private initLog() {
    this.messageLog.where ="correos";
    this.messageLog.tipo  = "service";
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
