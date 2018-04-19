import { BrowserModule } from '@angular/platform-browser';
import { FormsModule, ReactiveFormsModule }   from '@angular/forms';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AppComponent } from './app.component';
import { FactorService } from './shared/factor/factor.service';
import { HttpClientModule } from '@angular/common/http';
import { FactorListComponent } from './factor-list/factor-list.component';
import { MatButtonModule, MatCardModule, MatInputModule, MatListModule, MatGridListModule, MatToolbarModule } from '@angular/material';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

@NgModule({
  declarations: [
    AppComponent,
    FactorListComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    BrowserAnimationsModule,
    MatButtonModule,
    MatCardModule,
    MatInputModule,
    MatListModule,
    MatGridListModule,
    MatToolbarModule,
    FormsModule,
    ReactiveFormsModule, // why not?
    RouterModule
  ],
  providers: [FactorService],
  bootstrap: [AppComponent]
})
export class AppModule { }
