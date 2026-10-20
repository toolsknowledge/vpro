import { provideHttpClient } from '@angular/common/http';
import { ApplicationConfig, provideBrowserGlobalErrorListeners } from '@angular/core';

export const appConfig: ApplicationConfig = {
  // The default XHR backend is used (not withFetch) because fetch cannot report upload progress.
  providers: [provideBrowserGlobalErrorListeners(), provideHttpClient()],
};
