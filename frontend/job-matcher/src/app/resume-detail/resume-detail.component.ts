import { Component, Input } from '@angular/core';
import { Resume } from '../models/resume';
import { NgFor, NgIf } from '@angular/common';
import { POSData } from '../models/pos';
import { PosComponentComponent } from '../pos-component/pos-component.component';

@Component({
  selector: 'app-resume-detail',
  standalone: true,
  imports: [
    NgFor,
    NgIf,
    PosComponentComponent
  ],
  templateUrl: './resume-detail.component.html',
  styleUrl: './resume-detail.component.scss'
})
export class ResumeDetailComponent {
  @Input() resume?: Resume;

  getKeys(obj: POSData | undefined): string[] {
    if (!obj){
      return [];
    }
    return Object.keys(obj);
  }

}
