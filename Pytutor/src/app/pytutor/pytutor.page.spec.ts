import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { IonicModule } from '@ionic/angular';
import { ExploreContainerComponentModule } from '../explore-container/explore-container.module';

import { PytutorPage } from './pytutor.page';

describe('PytutorPage', () => {
  let component: PytutorPage;
  let fixture: ComponentFixture<PytutorPage>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [PytutorPage],
      imports: [IonicModule.forRoot(), ExploreContainerComponentModule]
    }).compileComponents();

    fixture = TestBed.createComponent(PytutorPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
