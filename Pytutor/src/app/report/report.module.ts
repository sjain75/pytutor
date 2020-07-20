import { IonicModule } from '@ionic/angular';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ReportPage } from './report.page';
import { ExploreContainerComponentModule } from '../explore-container/explore-container.module';

import { ReportPageRoutingModule } from './report-routing.module';

@NgModule({
  imports: [
    IonicModule,
    CommonModule,
    FormsModule,
    ExploreContainerComponentModule,
    ReportPageRoutingModule
  ],
  declarations: [ReportPage]
})
export class ReportPageModule {}
