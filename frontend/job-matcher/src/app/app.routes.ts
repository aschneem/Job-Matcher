import { Routes } from '@angular/router';
import { ResumesComponent } from './resumes/resumes.component';
import { SearchConfigComponent } from './search-config/search-config.component';
import { JobPostsComponent } from './job-posts/job-posts.component';
import { ComparePostResumeComponent } from './compare-post-resume/compare-post-resume.component';

export const routes: Routes = [
    { path: 'resume', component: ResumesComponent },
    { path: 'search', component: SearchConfigComponent},
    { path: 'posts', component: JobPostsComponent},
    { path: 'posts/:name', component: JobPostsComponent},
    { path: 'compare/:postID/:resumeName', component: ComparePostResumeComponent}
];
