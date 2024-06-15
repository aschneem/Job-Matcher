import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { AppSettings } from '../models/app-settings';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AppSettingsService {

  constructor(private http: HttpClient) { }

  public appSettings?: AppSettings;

  public loadSettings() {
    this.http.get<AppSettings>(environment.apiHost + '/settings')
      .subscribe(settings => this.appSettings = settings);
  }

}
