import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError, map, tap, } from 'rxjs/operators';
import { MessageService } from './message.service';
import {Message} from './interfaces/message.interface'

import { Observable } from 'rxjs/Observable';
import { of } from 'rxjs/observable/of';

 
@Injectable()
export class GMapsService { 

    messageLog = new Message();
    
    constructor(private http: HttpClient,
                private messageS: MessageService
     ) {
      this.initLog();
    } 
     

    getLatLan(address: string):Observable<any>{

     return this.http.get("https://maps.google.com/maps/api/geocode/json?address=" + address + "CA&key=AIzaSyAs3JCBHNrrurTXN6yK4t3ceg69iM6attY")
  //       .toPromise()
  //       .then((response) => { return Promise.resolve(response.json());})
  //       .catch((error) => { return Promise.resolve(error.json());});
     .pipe(
       tap( dato => this.log("getAllCorreos",5, 'fetched correos cantidad: '+dato)),
       catchError(this.handleError('Error buscando correos valor=${valor}',[]))
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
 
  


