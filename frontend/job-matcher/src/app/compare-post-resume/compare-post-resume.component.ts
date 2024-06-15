import { Component, OnInit } from '@angular/core';
import { CompareService } from '../services/compare.service';
import { ActivatedRoute } from '@angular/router';
import { CompareSectionComponent } from '../compare-section/compare-section.component';
import { NgIf } from '@angular/common';
import { ResumePostCompare } from '../models/resumePostCompare';

@Component({
  selector: 'app-compare-post-resume',
  standalone: true,
  imports: [
    CompareSectionComponent,
    NgIf
  ],
  templateUrl: './compare-post-resume.component.html',
  styleUrl: './compare-post-resume.component.scss'
})
export class ComparePostResumeComponent implements OnInit {
  constructor(private compareService: CompareService,
    private route: ActivatedRoute) {
      
    }

  data?: ResumePostCompare
  
  ngOnInit(): void {
    const postID = this.route.snapshot.paramMap.get("postID");
    const resumeName = this.route.snapshot.paramMap.get("resumeName");
    if (!postID || !resumeName) {
      console.log('Error Invalid Route');
    } else {
      this.loadCompareData(postID, resumeName);  
    }
  }

  loadCompareData(postID: string, resumeName: string) {
    this.compareService.getResumePostCompare(postID, resumeName).subscribe(data => {
      this.data = data;
    })
  }

}
