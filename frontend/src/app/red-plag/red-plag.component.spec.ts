import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RedPlagComponent } from './red-plag.component';

describe('RedPlagComponent', () => {
  let component: RedPlagComponent;
  let fixture: ComponentFixture<RedPlagComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ RedPlagComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RedPlagComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
