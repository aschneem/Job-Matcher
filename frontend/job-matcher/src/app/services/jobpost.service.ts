import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { JobPost } from '../models/jobpost';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class JobpostService {

  constructor(private http: HttpClient) { }

  getJobPosts(): Observable<JobPost[]> {
    return this.http.get<JobPost[]>(environment.apiHost + "/jobpost");
  }

  getJobPostsByStatus(status: string): Observable<JobPost[]> {
    return this.http.get<JobPost[]>(environment.apiHost + "/jobpost?status=" + status);
  }

  getJobPostsBySearch(name: string): Observable<JobPost[]> {
    return this.http.get<JobPost[]>(environment.apiHost + "/jobpost/s/" + name);
  }

  getJobPost(id: string): Observable<JobPost> {
    return this.http.get<JobPost>(environment.apiHost + '/jobpost/' + id);
  }

  updateStatus(id: string, status: string): Observable<{'result': boolean}> {
    return this.http.get<{'result': boolean}>(environment.apiHost + '/jobpost/' + id + '/status/' + status);
  }
}
