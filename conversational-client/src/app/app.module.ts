import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {RouterOutlet} from '@angular/router';

import {BrowserModule} from '@angular/platform-browser';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {HttpClientModule} from '@angular/common/http';

import {AppComponent} from './app.component';
import {SpeechRecognizerComponent} from '@components/speech-recognizer/speech-recognizer.component';
import {ModeSelectorComponent} from '@components/mode-selector/mode-selector.component';

import {MatButtonModule} from '@angular/material/button';
import {MatChipsModule} from '@angular/material/chips';
import {MatSidenavModule} from '@angular/material/sidenav';
import {MatIconModule} from '@angular/material/icon';
import {MatToolbarModule} from '@angular/material/toolbar';
import {MatList, MatListItem} from '@angular/material/list';
import {HistoryTutorComponent} from '@components/history-tutor/history-tutor.component';
import {FakeModeComponent} from '@components/fake-mode/fake-mode.component';

const materialModules = [
  MatButtonModule,
  MatChipsModule,
  MatIconModule,
  MatToolbarModule,
  MatSidenavModule,
  MatList,
  MatListItem,
];

@NgModule({
  declarations: [
    AppComponent,
    SpeechRecognizerComponent,
    ModeSelectorComponent,
    HistoryTutorComponent,
    FakeModeComponent,
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    CommonModule,
    HttpClientModule,
    RouterOutlet,
    ...materialModules,
  ],
  bootstrap: [AppComponent],
})
export class AppModule {}
