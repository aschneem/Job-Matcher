import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EntityDisplayComponent } from './entity-display.component';

describe('EntityDisplayComponent', () => {
  let component: EntityDisplayComponent;
  let fixture: ComponentFixture<EntityDisplayComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EntityDisplayComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(EntityDisplayComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
