import { Injectable } from '@angular/core';
import { SearchConfig } from '../models/search';
import { Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { StartSearchResponse } from '../models/start-search';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class SearchService {

  constructor(private http: HttpClient) { }

  getSearchConfigs(): Observable<SearchConfig[]> {
    return this.http.get<SearchConfig[]>(environment.apiHost + "/search");
  }

  getSearchConfig(name: string): Observable<SearchConfig> {
    return this.http.get<SearchConfig>(environment.apiHost + '/search/' + name);
  }

  runSearchConfig(name: string): Observable<StartSearchResponse> {
    return this.http.get<StartSearchResponse>(environment.apiHost + "/search/" + name + "/run");
  }

  runAllSearches(): Observable<StartSearchResponse> {
    return this.http.get<StartSearchResponse>(environment.apiHost + "/search/run");
  }

  uploadSearch(file: File): Observable<SearchConfig> {
    const data = new FormData();
    data.append('file', file, file.name);
    return this.http.post<SearchConfig>(environment.apiHost + '/search/upload', data);
  }
}
