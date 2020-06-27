import { IonicModule } from '@ionic/angular';
import { RouterModule } from '@angular/router';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { PytutorPage } from './pytutor.page';
import { ExploreContainerComponentModule } from '../explore-container/explore-container.module';

import { PytutorPageRoutingModule } from './pytutor-routing.module';

@NgModule({
  imports: [
    IonicModule,
    CommonModule,
    FormsModule,
    ExploreContainerComponentModule,
    PytutorPageRoutingModule
  ],
  declarations: [PytutorPage]
})
export class PytutorPageModule {}
