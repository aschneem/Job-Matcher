import { ComponentFixture, TestBed } from '@angular/core/testing';

import { KeywordDisplayComponent } from './keyword-display.component';

describe('KeywordDisplayComponent', () => {
  let component: KeywordDisplayComponent;
  let fixture: ComponentFixture<KeywordDisplayComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [KeywordDisplayComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(KeywordDisplayComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
