import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { MainComponent } from './main/main.component';
import { RankComponent } from './rank/rank.component';

const routes: Routes = [
  { 
    path: '', redirectTo: '/main', pathMatch: 'full' 
  },
  {
    path: "main", component: MainComponent, title: "Advisor"
  },
  {
    path: "rank", component: RankComponent, title: "Advisor"
  },
  // {
  //   path: "**", component: NotfoundComponent, title: "Not Founded"
  // },
];


@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
