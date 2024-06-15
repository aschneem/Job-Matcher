import { Component, OnInit, importProvidersFrom } from '@angular/core';
import { RouterLink, RouterOutlet } from '@angular/router';
import { ResumesComponent } from './resumes/resumes.component';
import { AppSettingsService } from './services/app-settings.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, ResumesComponent, RouterLink],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
})
export class AppComponent{

  constructor(){}

  title = 'Job Matcher';
}
