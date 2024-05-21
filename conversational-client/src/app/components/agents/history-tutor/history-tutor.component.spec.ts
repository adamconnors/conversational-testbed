import {ComponentFixture, TestBed} from '@angular/core/testing';

import {HistoryTutorComponent} from './history-tutor.component';

describe('HistoryTutorComponent', () => {
  let component: HistoryTutorComponent;
  let fixture: ComponentFixture<HistoryTutorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [HistoryTutorComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(HistoryTutorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

describe('HistoryTutorComponent', () => {
  let component: HistoryTutorComponent;

  it('should calculate %age questions answered', () => {
    component.worldState = {
      question: 'What is the capital of France?',
      answers: [
        {answer: 'Paris', hasAnswered: 'false'},
        {answer: 'London', hasAnswered: 'false'},
        {answer: 'Berlin', hasAnswered: 'false'},
      ],
    };

    expect(component.calculatePercentageComplete()).toBe(0);
  });
});
