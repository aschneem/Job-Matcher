import { Injectable } from '@angular/core';
import { Resume } from '../models/resume';
import { Observable, of } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ResumeService {

  constructor(private http: HttpClient) { }

  getResumes(): Observable<Resume[]> {
    return this.http.get<Resume[]>(environment.apiHost + "/resume");
  }

  getResume(name: string): Observable<Resume> {
    return this.http.get<Resume>(environment.apiHost + '/resume/' + name);
  }

  uploadResume(file: File): Observable<Resume> {
    const data = new FormData();
    data.append('file', file, file.name);
    return this.http.post<Resume>(environment.apiHost + '/resume/upload', data);
  }

  setDefault(name: string): Observable<Resume> {
    return this.http.post<Resume>(environment.apiHost + '/resume/' + name + "/default", {})
  }
}
