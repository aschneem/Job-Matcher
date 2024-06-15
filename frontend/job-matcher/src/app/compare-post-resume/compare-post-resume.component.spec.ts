import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ComparePostResumeComponent } from './compare-post-resume.component';

describe('ComparePostResumeComponent', () => {
  let component: ComparePostResumeComponent;
  let fixture: ComponentFixture<ComparePostResumeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ComparePostResumeComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ComparePostResumeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
