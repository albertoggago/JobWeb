/* tslint:disable:no-unused-variable */

import { TestBed, async, inject } from '@angular/core/testing';
import { CorreosService } from './correos.service';

describe('CorreosService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [CorreosService]
    });
  });

  it('should ...', inject([CorreosService], (service: CorreosService) => {
    expect(service).toBeTruthy();
  }));
});
