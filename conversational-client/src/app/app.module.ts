import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';

import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HttpClientModule } from '@angular/common/http';

import {AppComponent} from './app.component';
import { SpeechRecognizerComponent } from '@components/speech-recognizer/speech-recognizer.component';

import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import {MatToolbarModule} from '@angular/material/toolbar';

const materialModules = [MatButtonModule, MatIconModule, MatToolbarModule];

@NgModule({
  declarations: [
    AppComponent, SpeechRecognizerComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    CommonModule,
    HttpClientModule,
    RouterOutlet,
    ...materialModules
  ],
  bootstrap: [AppComponent],
})
export class AppModule { }
