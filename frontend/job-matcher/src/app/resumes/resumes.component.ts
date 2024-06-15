import { Component, OnInit } from '@angular/core';
import { Resume } from '../models/resume';
import { NgFor, NgIf } from '@angular/common';
import { POSData } from '../models/pos';
import { ResumeService } from '../services/resume.service';
import { ResumeDetailComponent } from '../resume-detail/resume-detail.component';
import { FileUploadComponent } from '../file-upload/file-upload.component';

@Component({
  selector: 'app-resumes',
  standalone: true,
  imports: [
    NgFor,
    NgIf,
    ResumeDetailComponent,
    FileUploadComponent
  ],
  templateUrl: './resumes.component.html',
  styleUrl: './resumes.component.scss'
})
export class ResumesComponent implements OnInit{
  constructor(private resumeService: ResumeService) {}

  resumes: Resume[] = [];
  selectedResume?: Resume;

  ngOnInit(): void {
    this.getResumes();
  }

  getResumes(): void {
    this.resumeService.getResumes()
      .subscribe(resumes => this.resumes = resumes);
  }

  onSelect(resume: Resume): void {
    this.selectedResume = resume;
  }

  uploadResume(fileList: FileList){
    if (fileList.length > 0) {
      const file = fileList.item(0);
      if (!file){
        return;
      }
      this.resumeService.uploadResume(file).subscribe(resume => {
        this.resumes.push(resume);
      })
    }
  }

  setDefault(name: string) {
    this.resumeService.setDefault(name).subscribe(
      value => console.log(value)
    );
  }
}
