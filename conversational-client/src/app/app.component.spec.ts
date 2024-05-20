import {TestBed} from '@angular/core/testing';
import {AppComponent} from './app.component';
import {HttpClientTestingModule} from '@angular/common/http/testing';
import {RouterModule} from '@angular/router';
import {MatSidenavModule} from '@angular/material/sidenav';
import {MatToolbarModule} from '@angular/material/toolbar';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {AgentSelectorComponent} from '@components/agent-selector/agent-selector.component';
import {SpeechRecognizerComponent} from '@components/speech-recognizer/speech-recognizer.component';
import {MatIconModule} from '@angular/material/icon';
import {MatListModule} from '@angular/material/list';
describe('AppComponent', () => {
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [
        AppComponent,
        AgentSelectorComponent,
        SpeechRecognizerComponent,
      ],
      imports: [
        HttpClientTestingModule,
        RouterModule.forRoot([]),
        MatListModule,
        MatIconModule,
        MatToolbarModule,
        MatSidenavModule,
        BrowserAnimationsModule,
      ],
    }).compileComponents();
  });

  it('should create', () => {
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.componentInstance;
    expect(app).toBeTruthy();
  });
});
