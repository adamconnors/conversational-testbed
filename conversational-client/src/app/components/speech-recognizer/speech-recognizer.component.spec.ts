import {ComponentFixture, TestBed} from '@angular/core/testing';
import {MatIconModule} from '@angular/material/icon';
import {SpeechRecognizerComponent} from './speech-recognizer.component';

describe('SpeechRecognizerComponent', () => {
  let component: SpeechRecognizerComponent;
  let fixture: ComponentFixture<SpeechRecognizerComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [SpeechRecognizerComponent],
      imports: [MatIconModule],
    }).compileComponents();

    fixture = TestBed.createComponent(SpeechRecognizerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
