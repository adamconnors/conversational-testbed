import {ComponentFixture, TestBed} from '@angular/core/testing';

import {FakeModeComponent} from './fake-mode.component';

describe('FakeModeComponent', () => {
  let component: FakeModeComponent;
  let fixture: ComponentFixture<FakeModeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FakeModeComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(FakeModeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
