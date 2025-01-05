import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { ToolbarComponent } from './toolbar/toolbar.component';
import { MainComponent } from './main/main.component';
import { FormsModule } from '@angular/forms';
import { ServiceMain } from './service.main';
import { HttpClientModule } from '@angular/common/http';
import { RankComponent } from './rank/rank.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
// import { NgToastModule } from 'ng-angular-popup';

// NgToastModule
@NgModule({
  declarations: [
    AppComponent,
    ToolbarComponent,
    MainComponent,
    RankComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    HttpClientModule,
    BrowserAnimationsModule,
    // NgToastModule,
  ],
  providers: [ServiceMain],
  bootstrap: [AppComponent]
})
export class AppModule { }
