import { Component } from '@angular/core';
import { JobpostService } from '../services/jobpost.service';
import { JobPost } from '../models/jobpost';
import { NgFor, NgIf } from '@angular/common';
import { JobPostDetailsComponent } from '../job-post-details/job-post-details.component';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { AppSettingsService } from '../services/app-settings.service';
import { AppSettings } from '../models/app-settings';

@Component({
  selector: 'app-job-posts',
  standalone: true,
  imports: [
    NgIf,
    NgFor,
    JobPostDetailsComponent,
    RouterLink
  ],
  templateUrl: './job-posts.component.html',
  styleUrl: './job-posts.component.scss'
})
export class JobPostsComponent {
  constructor(private jobPostService: JobpostService,
    private route: ActivatedRoute,
    public appSettingsService: AppSettingsService) {}

  posts: JobPost[] = [];
  selectedPost?: JobPost;

  ngOnInit(): void {
    const name = this.route.snapshot.paramMap.get("name");
    const status = this.route.snapshot.queryParamMap.get('status');
    console.log("name " + name + " status " + status);
    if (name !== null) {
      this.getJobPostsBySearch(name);
    } else if (status) {
      this.getJobPostsByStatus(status);
    } else {
      this.getJobPosts();
    }
  }

  getJobPostsBySearch(name: string): void {
    console.log('getJobPostsBySearch');
    this.jobPostService.getJobPostsBySearch(name)
      .subscribe(posts => this.posts = posts);
  }

  getJobPosts(): void {
    this.jobPostService.getJobPosts()
      .subscribe(posts => this.posts = posts);
  }

  getJobPostsByStatus(status: string): void {
    console.log('getJobPostsByStatus');
    this.jobPostService.getJobPostsByStatus(status)
      .subscribe(posts => this.posts = posts);
  }

  updatePostStatus(id:string, status:string): void {
    this.jobPostService.updateStatus(id, status)
      .subscribe(result => console.log(result));
  }

  onSelect(post: JobPost): void {
    this.selectedPost = post;
  }
}
