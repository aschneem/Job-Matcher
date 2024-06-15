import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SearchConfigDetailsComponent } from './search-config-details.component';

describe('SearchConfigDetailsComponent', () => {
  let component: SearchConfigDetailsComponent;
  let fixture: ComponentFixture<SearchConfigDetailsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SearchConfigDetailsComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(SearchConfigDetailsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
