import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PosComponentComponent } from './pos-component.component';

describe('PosComponentComponent', () => {
  let component: PosComponentComponent;
  let fixture: ComponentFixture<PosComponentComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PosComponentComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(PosComponentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
