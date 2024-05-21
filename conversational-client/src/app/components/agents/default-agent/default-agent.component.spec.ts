import {ComponentFixture, TestBed} from '@angular/core/testing';

import {DefaultAgentComponent} from './default-agent.component';

describe('DefaultAgentComponent', () => {
  let component: DefaultAgentComponent;
  let fixture: ComponentFixture<DefaultAgentComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [DefaultAgentComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(DefaultAgentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
