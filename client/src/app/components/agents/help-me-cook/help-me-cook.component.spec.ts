import {ComponentFixture, TestBed} from '@angular/core/testing';

import {HelpMeCookComponent} from './help-me-cook.component';

describe('HelpMeCookComponent', () => {
  let component: HelpMeCookComponent;
  let fixture: ComponentFixture<HelpMeCookComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [HelpMeCookComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(HelpMeCookComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
