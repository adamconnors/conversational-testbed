import {ComponentFixture, TestBed} from '@angular/core/testing';

import {PhysicsExpertComponent} from './physics-expert.component';

describe('PhysicsExpertComponent', () => {
  let component: PhysicsExpertComponent;
  let fixture: ComponentFixture<PhysicsExpertComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PhysicsExpertComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(PhysicsExpertComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
