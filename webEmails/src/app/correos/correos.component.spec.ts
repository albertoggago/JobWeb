/* tslint:disable:no-unused-variable */
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { DebugElement } from '@angular/core';

import { CorreosComponent } from './correos.component';

describe('CorreosComponent', () => {
  let component: CorreosComponent;
  let fixture: ComponentFixture<CorreosComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CorreosComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CorreosComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
