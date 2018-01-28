import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import {Router} from '@angular/router';
import { catchError, tap } from 'rxjs/operators';
import { MessageService } from './message.service';
import { GeneralService } from './general.service';

import { Observable } from 'rxjs/Observable';
import { of } from 'rxjs/observable/of';

import {Correo} from './interfaces/correo.interface';
import {Message} from './interfaces/message.interface';

const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json' })
};


@Injectable()
export class CorreosService {

messageLog = new Message();

private Path: String = "";

    constructor(
  	 private http: HttpClient,
  	 private _router: Router,
  	 private messageS: MessageService,
     private general: GeneralService
  	 ) {
      this.initLog();
      this.Path = general.getPathBase();
    }


  


   getAllCorreos(valor:string, skip:number,palabras:string): Observable<Correo[]> {
      this.log("getAllCorreos",3,"LOG");
   		if (palabras == "") {palabras = "XXX";}
    	const url = this.Path+'/correourls/tipo/'+valor+'/skip/'+skip+'/palabras/'+palabras;
    	return this.http.get<Correo[]>(url)
    		.pipe(
          	tap( correos => this.log("getAllCorreos",5, 'fetched correos cantidad: '+correos.length)),
        	catchError(this.handleError('Error buscando correos valor ${valor}',[]))
    		);
  }

  setCorreo(correo: Correo) : Observable<any>{
    this.log("setCorreos",3,"LOG");

    const url = this.Path+'/correourls/'+correo._id;
    this.log("setCorreos",4,`Set Correo url: `+url);
    
    return this.http.put<Correo>(url,correo, httpOptions).pipe(
    tap((correo: Correo) => this.log("setCorreos",5,`modify  w/ id=${correo._id}`)),
      catchError(this.handleError<Correo>('modifyCorreo'))
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
