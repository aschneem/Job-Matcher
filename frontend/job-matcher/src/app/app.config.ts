import { APP_INITIALIZER, ApplicationConfig, importProvidersFrom } from '@angular/core';
import { provideRouter } from '@angular/router';

import { routes } from './app.routes';
import { HttpClientModule } from '@angular/common/http';
import { AppSettingsService } from './services/app-settings.service';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes), 
    importProvidersFrom(HttpClientModule),
    {
      provide: APP_INITIALIZER,
      useFactory: (appSettingsService: AppSettingsService) => {
        appSettingsService.loadSettings();
      },
      deps: [AppSettingsService]
    }
  ]
};
