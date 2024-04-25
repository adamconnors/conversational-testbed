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
