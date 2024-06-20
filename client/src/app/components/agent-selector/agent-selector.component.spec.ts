import {ComponentFixture, TestBed} from '@angular/core/testing';
import {AgentSelectorComponent} from './agent-selector.component';
import {MatListModule} from '@angular/material/list';

describe('AgentSelectorComponent', () => {
  let component: AgentSelectorComponent;
  let fixture: ComponentFixture<AgentSelectorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [AgentSelectorComponent],
      imports: [MatListModule],
    }).compileComponents();

    fixture = TestBed.createComponent(AgentSelectorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
