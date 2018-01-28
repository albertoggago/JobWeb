import { Injectable } from '@angular/core';

@Injectable()
export class GeneralService {

  constructor() { }

  //private pathBase: string = 'http://localhost:3001'+'/api/v2';
  private pathBase: string = 'http://localhost:3001'+'/api/v2';

  getPathBase () {
  	return this.pathBase;
  }

}
