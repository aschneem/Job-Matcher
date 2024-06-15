import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ResumePostCompare } from '../models/resumePostCompare';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class CompareService {

  constructor(private http: HttpClient) { }

  getResumePostCompare(postID: string, resumeName: string): Observable<ResumePostCompare> {
    return this.http.get<ResumePostCompare>(environment.apiHost + "/compare/" + postID + "/" + resumeName)
  }

}
