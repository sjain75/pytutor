import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { PytutorPage } from './pytutor.page';

const routes: Routes = [
  {
    path: '',
    component: PytutorPage,
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class PytutorPageRoutingModule {}
