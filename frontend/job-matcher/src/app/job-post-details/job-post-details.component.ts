import { Component, Input } from '@angular/core';
import { JobPost } from '../models/jobpost';
import { POSData } from '../models/pos';
import { NgFor, NgIf } from '@angular/common';
import { PosComponentComponent } from '../pos-component/pos-component.component';
import { KeywordDisplayComponent } from '../keyword-display/keyword-display.component';
import { EntityDisplayComponent } from '../entity-display/entity-display.component';

@Component({
  selector: 'app-job-post-details',
  standalone: true,
  imports: [
    NgFor,
    NgIf,
    PosComponentComponent,
    KeywordDisplayComponent,
    EntityDisplayComponent
  ],
  templateUrl: './job-post-details.component.html',
  styleUrl: './job-post-details.component.scss'
})
export class JobPostDetailsComponent {
  @Input() post?: JobPost;

  getKeys(obj: POSData | undefined): string[] {
    if (!obj){
      return [];
    }
    return Object.keys(obj);
  }
}
