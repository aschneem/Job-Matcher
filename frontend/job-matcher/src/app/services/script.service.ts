import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { Script } from '../models/script';

@Injectable({
  providedIn: 'root'
})
export class ScriptService {

  constructor(private http: HttpClient) { }

  getScripts(): Observable<Script[]> {
    return this.http.get<Script[]>(environment.apiHost + "/script");
  }

  getScript(name: string): Observable<Script> {
    return this.http.get<Script>(environment.apiHost + "/script/" + name);
  }

  updateScript(name: string, script: Script): Observable<Script> {
    return this.http.post<Script>(environment.apiHost + "/script/" + name, script);
  }

}
