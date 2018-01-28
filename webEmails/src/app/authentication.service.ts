import { Injectable } from '@angular/core';
import {Router} from '@angular/router';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError, map, tap } from 'rxjs/operators';
import { MessageService } from './message.service';
import { GeneralService } from './general.service';

import { Observable } from 'rxjs/Observable';
import { of } from 'rxjs/observable/of';

import {User} from './interfaces/user.interface'
import {Message} from './interfaces/message.interface'

declare var CryptoJS:any;

@Injectable()
export class AuthenticationService {

messageLog :Message = new Message();

  private Path: String ="";
  
  constructor(
  	 private http: HttpClient,
  	 private _router: Router,
  	 private messageS: MessageService,
     private general: GeneralService
  	 ) {
    this.initLog();
    this.Path = general.getPathBase()+'/userLogin/email/';
  }

  //private Path: String = 'http://92.191.223.89:3001'+'/api/v2'+'/userLogin/email/';
  
  private result : boolean = false;
  
  authPath : string = "auth";
  
  logout() {
    this.log("logout",3,"LOG");
    localStorage.removeItem("userAGG");
    localStorage.removeItem("hashDBAGG");
    this._router.navigate([this.authPath]); 
  }


 
  login(user: User, navigate:string, tipo:number){
    this.log("login",3,"LOG");

      if (tipo == 0)
        {user.hashDB = CryptoJS.MD5(user.password).toString();}
      this.verifyUser(user).subscribe(datos => {
        this.log("login",5,"datos: "+JSON.stringify(datos));
        this.log("login",5,"user: "+JSON.stringify(datos));
      	if (typeof datos === "undefined") {
          this.log("login",1,"No existe el usuario o el servicio no funcionaxxx");

          user.errorMsg = "No existe el usuario o el servicio no funcionaxxx"  
          this._router.navigate([this.authPath]);
        } else if (user.hashDB == datos.hashDB){ 
          this.log("login",5,"localStorage "+user.email+" : "+user.hashDB);

	  		  localStorage.setItem("userAGG", user.email);
          localStorage.setItem("hashDBAGG", user.hashDB);
          this._router.navigate([navigate]);
        } else {
          user.errorMsg = "No existe el usuario o el servicio no funciona"
          this._router.navigate([this.authPath]);
        }
			
    });
  }
 
   checkCredentials(pagina: string){
    this.log("checkCredentials",3,"LOG");
    if (localStorage.getItem("userAGG") === null){
        this.log("checkCredentials",4,"SIN CREDENTIALs go to Auth");
        this._router.navigate([this.authPath]);
    } else {
      this.log("checkCredentials",4,"OK");
      var userX = new User();
      userX.email = localStorage.getItem("userAGG");
      userX.hashDB = localStorage.getItem("hashDBAGG");
      this.log("checkCredentials",5,"user x:"+JSON.stringify(userX));
      this.login(userX,pagina,1);
    }
  }

    verifyUser(user: User): Observable<User> {
      this.log("verifyUser",3,"LOG");
    	const url = this.Path+user.email.toLowerCase();
      this.log("verifyUser",3,"url: "+url);
    	return this.http.get<User>(url)
    		.pipe(
    			//map(user => user[0]),
         tap( _ => this.log("checkCredentials",5,`fetched user ${user.email}`)),
       	catchError(this.handleError<User>(`Error buscando usuario user ${user.email} ${url}`))
    		);
  }

  goAuthPage(){
    this.log("goAuthPage",3,"LOG");
    this._router.navigate([this.authPath]);
  }

  
  private handleError<T> (operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {

      // TODO: send the error to remote logging infrastructure
      console.error(error); // log to console instead

      // TODO: better job of transforming error for user consumption
      this.log("handleError",1,`${operation} failed: ${error.message}`);

      // Let the app keep running by returning an empty result.
      return of(result as T);
    };
  }

  private initLog() {
    this.messageLog.where   ="authentication";
    this.messageLog.tipo    = "service";
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
