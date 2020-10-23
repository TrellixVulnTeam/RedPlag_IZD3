import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PasswordDeleteComponent } from './password-delete.component';

describe('PasswordDeleteComponent', () => {
  let component: PasswordDeleteComponent;
  let fixture: ComponentFixture<PasswordDeleteComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PasswordDeleteComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PasswordDeleteComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
