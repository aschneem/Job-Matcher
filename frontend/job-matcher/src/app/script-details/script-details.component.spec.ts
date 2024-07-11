import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ScriptDetailsComponent } from './script-details.component';

describe('ScriptDetailsComponent', () => {
  let component: ScriptDetailsComponent;
  let fixture: ComponentFixture<ScriptDetailsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ScriptDetailsComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ScriptDetailsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
