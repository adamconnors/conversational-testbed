import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {RouterOutlet, RouterModule, Routes} from '@angular/router';

import {BrowserModule} from '@angular/platform-browser';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {HttpClientModule} from '@angular/common/http';

import {AppComponent} from './app.component';
import {SpeechRecognizerComponent} from '@components/speech-recognizer/speech-recognizer.component';
import {AgentSelectorComponent} from '@components/agent-selector/agent-selector.component';

import {MatButtonModule} from '@angular/material/button';
import {MatChipsModule} from '@angular/material/chips';
import {MatSidenavModule} from '@angular/material/sidenav';
import {MatIconModule} from '@angular/material/icon';
import {MatToolbarModule} from '@angular/material/toolbar';
import {MatCardModule} from '@angular/material/card';
import {MatList, MatListItem} from '@angular/material/list';
import {HistoryTutorComponent} from '@components/agents/history-tutor/history-tutor.component';
import {FakeAgentComponent} from '@components/agents/fake-agent/fake-agent.component';

export const routes: Routes = [
  {
    path: '',
    component: AppComponent,
  },
];

const materialModules = [
  MatButtonModule,
  MatChipsModule,
  MatIconModule,
  MatToolbarModule,
  MatSidenavModule,
  MatList,
  MatListItem,
  MatCardModule,
];

@NgModule({
  declarations: [
    AppComponent,
    SpeechRecognizerComponent,
    AgentSelectorComponent,
    HistoryTutorComponent,
    FakeAgentComponent,
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    CommonModule,
    HttpClientModule,
    RouterModule.forRoot(routes),
    RouterOutlet,
    ...materialModules,
  ],
  bootstrap: [AppComponent],
})
export class AppModule {}
