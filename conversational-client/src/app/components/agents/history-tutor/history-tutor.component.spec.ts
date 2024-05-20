import {ComponentFixture, TestBed} from '@angular/core/testing';

import {HistoryTutorComponent, WorldState} from './history-tutor.component';

describe('HistoryTutorComponent', () => {
  let component: HistoryTutorComponent;
  let fixture: ComponentFixture<HistoryTutorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [HistoryTutorComponent],
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
    // Zero percent.
    component = new HistoryTutorComponent();
    component.worldState = {
      question: 'What is the capital of France?',
      answers: [
        {answer: 'Paris', hasAnswered: 'false'},
        {answer: 'London', hasAnswered: 'false'},
        {answer: 'Berlin', hasAnswered: 'false'},
      ],
    } as WorldState;

    expect(component.calculatePercentageComplete()).toBe(0);

    // 33 percent.
    component.worldState.answers[0].hasAnswered = 'true';
    expect(component.calculatePercentageComplete()).toBe(33);
  });
});
