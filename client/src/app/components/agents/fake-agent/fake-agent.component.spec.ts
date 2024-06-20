import {ComponentFixture, TestBed} from '@angular/core/testing';

import {FakeAgentComponent} from './fake-agent.component';

describe('FakeAgentComponent', () => {
  let component: FakeAgentComponent;
  let fixture: ComponentFixture<FakeAgentComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [FakeAgentComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(FakeAgentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
