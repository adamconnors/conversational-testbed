import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SpeechRecognizerComponent } from './speech-recognizer.component';

describe('SpeechRecognizerComponent', () => {
  let component: SpeechRecognizerComponent;
  let fixture: ComponentFixture<SpeechRecognizerComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SpeechRecognizerComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(SpeechRecognizerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
